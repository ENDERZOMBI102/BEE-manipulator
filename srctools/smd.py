"""Parses SMD model/animation data."""
import os
import re
from operator import itemgetter

import math
from typing import (
    List, Optional, Dict, Tuple, Iterator, Iterable, Union,
    BinaryIO,
)

from srctools import Vec


class Bone:
    """Represents a single bone."""
    __slots__ = ('name', 'parent')

    def __init__(self, name: str, parent: Optional['Bone']):
        self.name = name
        self.parent = parent

    def __repr__(self) -> str:
        return '<Bone "{}", parent={}>'.format(
            self.name,
            self.parent.name
            if self.parent else
            'None',
        )


class BoneFrame:
    """Represents a single frame of bone animation."""
    __slots__ = ('bone', 'position', 'rotation')

    def __init__(self, bone: Bone, position: Vec, rotation: Vec):
        self.bone = bone
        self.position = position
        self.rotation = rotation


class Vertex:
    """A single vertex."""
    __slots__ = ('pos', 'norm', 'tex_u', 'tex_v', 'links')
    def __init__(
        self,
        pos: Vec,
        norm: Vec,
        tex_u: float,
        tex_v: float,
        links: List[Tuple[Bone, float]],
    ):
        self.pos = pos
        self.norm = norm
        self.links = links
        self.tex_u = tex_u
        self.tex_v = tex_v

    def __repr__(self) -> str:
        return 'Vertex({!r}, {!r}, {}, {}, {})'.format(
            self.pos, self.norm, self.tex_u, self.tex_v, self.links
        )

    def copy(self) -> 'Vertex':
        return Vertex(
            self.pos.copy(),
            self.norm.copy(),
            self.tex_u,
            self.tex_v,
            self.links.copy(),
        )


class Triangle:
    """Represents one triangle."""
    __slots__ = ('mat', 'point1', 'point2', 'point3')

    def __init__(self, mat: str, p1: Vertex, p2: Vertex, p3: Vertex):
        self.mat = mat
        self.point1 = p1
        self.point2 = p2
        self.point3 = p3

    def __iter__(self) -> Iterator[Vertex]:
        yield self.point1
        yield self.point2
        yield self.point3

    def __len__(self) -> int:
        return 3

    def __getitem__(self, item: int) -> Vertex:
        if item == 0:
            return self.point1
        elif item == 1:
            return self.point2
        elif item == 2:
            return self.point3
        else:
            raise IndexError(item)

    def __setitem__(self, item: int, value: Vertex) -> None:
        if not isinstance(value, Vertex):
            raise ValueError('Points can only be vertices!')

        if item == 0:
            self.point1 = value
        elif item == 1:
            self.point2 = value
        elif item == 2:
            self.point3 = value
        else:
            raise IndexError(item)

    def copy(self) -> 'Triangle':
        """Duplicate this triangle."""
        return Triangle(
            self.mat,
            self.point1.copy(),
            self.point2.copy(),
            self.point3.copy(),
        )


class ParseError(Exception):
    """Invalid model format."""
    def __init__(self, line_num: Union[int, str], msg: str, *args: object):
        super(ParseError, self).__init__('{}: {}'.format(
            line_num,
            msg.format(*args),
        ))


def _clean_file(file: Iterable[bytes]) -> Iterator[Tuple[int, bytes]]:
    line_num = 0
    for line in file:
        line_num += 1
        if b'//' in line:
            line = line.split(b'//', 1)[0]
        if b'#' in line:
            line = line.split(b'#', 1)[0]
        if b';' in line:
            line = line.split(b';', 1)[0]
        line = line.strip()
        if line:
            yield line_num, line


class Mesh:
    """The contents of an SMD model.

    This contains:
    * A bone tree
    * Animation frames
    * Optionally triangle data.
    """
    def __init__(
        self,
        bones: Dict[str, Bone],
        animation: Dict[int, List[BoneFrame]],
        triangles: List[Triangle]
    ) -> None:
        self.bones = bones
        self.animation = animation
        self.triangles = triangles

    @staticmethod
    def blank(root_name: str) -> 'Mesh':
        """Create an empty mesh, with a single root bone."""
        root_bone = Bone(root_name, None)
        return Mesh(
            {root_name: root_bone},
            {0: [
                BoneFrame(root_bone, Vec(), Vec())
            ]},
            [],
        )

    @staticmethod
    def parse_smd(file: Iterable[bytes]) -> 'Mesh':
        """Parse a SMD file.

        The file argument should be an iterable of lines.
        It is parsed in binary, since non-ASCII characters are not
        permitted in SMDs.
        """
        file_iter = _clean_file(file)

        bones = None
        anim = None
        tri = None

        line_num = 1

        for line_num, line in file_iter:
            if line.startswith(b'version'):
                version = line.split(None, 1)[1]
                if version != b'1':
                    raise ParseError(
                        line_num,
                        'Unknown version {}!',
                        version,
                    )
            elif line == b'nodes':
                if bones is not None:
                    raise ParseError(
                        line_num,
                        'Duplicate bone section!',
                    )
                bones = Mesh._parse_smd_bones(file_iter)
            elif line == b'skeleton':
                if anim is not None:
                    raise ParseError(
                        line_num,
                        'Duplicate animation section!',
                    )
                anim = Mesh._parse_smd_anim(file_iter, bones)
            elif line == b'triangles':
                if tri is not None:
                    raise ParseError(
                        line_num,
                        'Duplicate triangle section!',
                    )
                elif bones is None:
                    raise ParseError(
                        line_num,
                        'Triangles section before bones section!'
                    )
                tri = Mesh._parse_smd_tri(file_iter, bones)

        if bones is None:
            raise ParseError(line_num, 'No bone section!')

        if anim is None:
            raise ParseError(line_num, 'No animation section!')

        if tri is None:
            tri = []

        return Mesh({
            bone.name: bone
            for bone in
            bones.values()
        }, anim, tri)

    @staticmethod
    def _parse_smd_bones(file_iter: Iterator[Tuple[int, bytes]]) -> Dict[int, Bone]:
        """Parse the 'nodes' section of SMDs."""
        bones = {}
        for line_num, line in file_iter:
            if line == b'end':
                return bones
            try:
                bone_ind, bone_name, bone_parent = re.fullmatch(
                    br'([0-9]+)\s*"([^"]*)"\s*(-?[0-9]+)',
                    line,
                ).groups()
                bone_ind = int(bone_ind)
                bone_parent = int(bone_parent)
            except (ValueError, AttributeError):  # None.groups()
                raise ParseError(line_num, 'Invalid line!') from None
            else:
                if bone_parent == -1:
                    parent_ind = None
                else:
                    try:
                        parent_ind = bones[bone_parent]
                    except KeyError:
                        raise ParseError(
                            line_num,
                            'Undefined parent bone {}!',
                            bone_parent,
                        ) from None
                bones[bone_ind] = Bone(bone_name.decode('ascii'), parent_ind)
        raise ParseError('end', 'No end to nodes section!')

    @staticmethod
    def _parse_smd_anim(file_iter: Iterator[Tuple[int, bytes]], bones: Dict[int, Bone]):
        """Parse the 'skeleton' section of SMDs."""
        frames = {}
        time = -999999999
        for line_num, line in file_iter:
            if line.startswith((b'//', b'#', b';')):
                continue
            if line.startswith(b'time'):
                try:
                    time = int(line[4:])
                except ValueError:
                    raise ParseError(line_num, 'Invalid time value!') from None
                if time in frames:
                    raise ValueError(line_num, 'Duplicate frame time {}!', time)
                frames[time] = []
            elif line == b'end':
                return frames
            else:  # Bone.
                try:
                    byt_ind, byt_x, byt_y, byt_z, byt_pit, byt_yaw, byt_rol = line.split()
                    pos = Vec(float(byt_x), float(byt_y), float(byt_z))
                    rot = Vec(float(byt_pit), float(byt_yaw), float(byt_rol))
                except ValueError:
                    raise ParseError(line_num, 'Invalid line!') from None
                try:
                    bone = bones[int(byt_ind)]
                except KeyError:
                    raise ParseError(line_num, 'Unknown bone index {}!', int(byt_ind))
                frames[time].append(BoneFrame(bone, pos, rot))

        raise ParseError('end', 'No end to skeleton section!')

    @staticmethod
    def _parse_smd_tri(file_iter: Iterator[Tuple[int, bytes]], bones: Dict[int, Bone]):
        """Parse the 'triangles' section of SMDs."""
        tris = []
        points = [None, None, None]
        for line_num, line in file_iter:
            if line == b'end':
                return tris
            try:
                mat_name = line.decode('ascii')
            except UnicodeDecodeError as exc:
                raise ParseError(
                    line_num,
                    'Non-ASCII material: {} at position {} - {}',
                    exc.reason,
                    exc.start
                ) from None

            # We need to process the material name, it can have various things
            # in it - ignored folders, file extensions.
            mat_name = os.path.basename(mat_name.rstrip('\\/ \t\b\n\r'))

            # Grab the three lines.
            for i in range(3):
                try:
                    line_num, line = next(file_iter)
                except StopIteration:
                    raise ParseError('end', 'Incomplete triangles!')
                try:
                    (
                        byt_parent,
                        x, y, z,
                        nx, ny, nz,
                        byt_tex_u, byt_tex_v,
                        *links_raw,
                    ) = line.split()
                except ValueError:
                    raise ParseError(line_num, 'Not enough values!')
                try:
                    pos = Vec(float(x), float(y), float(z))
                    norm = Vec(float(nx), float(ny), float(nz))
                except ValueError:
                    raise ParseError(line_num, 'Invalid normal or position!')
                try:
                    tex_u = float(byt_tex_u)
                    tex_v = float(byt_tex_v)
                except ValueError:
                    raise ParseError(line_num, 'Invalid texture UV!')

                try:
                    parent = bones[int(byt_parent)]
                except KeyError:
                    raise ParseError(line_num, 'Invalid bone {}!', int(byt_parent))

                if links_raw:
                    link_count = int(links_raw[0])

                    if (link_count * 2 + 1) != len(links_raw):
                        raise ParseError(line_num, 'Extra weight number: {}', links_raw)

                    links = []
                    for off in range(1, len(links_raw), 2):
                        try:
                            bone = bones[int(links_raw[off])]
                        except KeyError:
                            raise ParseError(line_num, 'Unknown bone {}!', links_raw[off])
                        links.append((bone, float(links_raw[off+1])))
                    remainder = 1.0 - math.fsum(weight for bone, weight in links)
                    if remainder:
                        links.append((parent, remainder))
                else:
                    links = [(parent, 1.0)]

                points[i] = Vertex(pos, norm, tex_u, tex_v, links)
            tris.append(Triangle(mat_name, *points))

        raise ParseError('end', 'No end to triangles section!')

    def export(self, file: BinaryIO):
        """Write out the SMD to the given file."""
        file.write(b"version 1\nnodes\n")

        # Deconstruct the tree into the original indexes.
        bone_indexes = {}  # type: Dict[Bone, int]
        next_ind = 0
        todo = set(self.bones.values())
        while todo:
            for bone in todo:
                if not bone.parent or bone.parent in bone_indexes:
                    bone_indexes[bone] = next_ind
                    todo.remove(bone)
                    if bone.parent is None:
                        parent_ind = -1
                    else:
                        parent_ind = bone_indexes[bone.parent]  # or KeyError.
                    file.write(b'%i "%s" %i\n' % (
                        next_ind,
                        bone.name.encode('ascii'),
                        parent_ind,
                    ))
                    next_ind += 1
                    break
            else:
                # Every bone had a parent, so it must be a loop somewhere!
                raise ValueError('Loop in bone parenting!')

        file.write(b'end\nskeleton\n')
        for time, frame in sorted(self.animation.items(), key=itemgetter(0)):
            file.write(b'time %i\n' % time)
            for bone_pose in frame:  # type: BoneFrame
                x, y, z = bone_pose.position
                pit, yaw, rol = bone_pose.rotation
                file.write(b'%i %.6f %.6f %.6f  %.6f %.6f %.6f\n' % (
                    bone_indexes[bone_pose.bone],
                    x, y, z,
                    pit, yaw, rol,
                ))
        file.write(b'end\n')
        if self.triangles:
            file.write(b'triangles\n')
            for tri in self.triangles:
                file.write(tri.mat.encode('ascii') + b'\n')
                for vert in tri:
                    # Add the last link as the "main" one, which recieves
                    # the amount not set by the other weights.
                    assert len(vert.links) > 0
                    file.write(
                        b'%i\t%.6f %.6f %.6f\t'  # bone index, position XYZ
                        b'%.6f %.6f %.6f\t'  # Normal XYZ
                        b'%.6f %.6f %i' % (  # UV, weight count.
                            bone_indexes[vert.links[-1][0]],
                            vert.pos.x, vert.pos.y, vert.pos.z,
                            vert.norm.x, vert.norm.y, vert.norm.z,
                            vert.tex_u, vert.tex_v, (len(vert.links) - 1)
                        )
                    )
                    for bone, weight in vert.links[:-1]:
                        file.write(b' %i %.6f' % (bone_indexes[bone], weight))
                    file.write(b'\n')
            file.write(b'end\n')

    def append_model(
        self,
        mdl: 'Mesh',
        rotation: Vec=(0.0, 0.0, 0.0),
        offset: Vec=(0.0, 0.0, 0.0),
        scale: float=1.0,
    ) -> None:
        """Append another model's geometry onto this one.

        All geometry is attached to the root bone.
        """
        if not mdl.triangles:
            # Nothing to add.
            return

        for bone in self.bones.values():
            if bone.parent is None:
                root_bone = bone
                break
        else:
            raise ValueError('No root bone?')

        bone_link = [(root_bone, 1.0)]

        for orig_tri in mdl.triangles:
            new_tri = orig_tri.copy()
            for vert in new_tri:
                vert.links[:] = bone_link

                vert.norm.rotate(*rotation, round_vals=False)
                vert.pos *= scale
                vert.pos.rotate(*rotation, round_vals=False)
                vert.pos += offset

            self.triangles.append(new_tri)

    # The triangles required for a prism.
    # Each sublist is a triangle.
    # The tuples are (x, y, z, u, v).
    _BBOX_MESH_DATA = [
        [
            (-1, -1, -1, 0.0, 0.0),
            (-1, +1, +1, 1.0, 1.0),
            (-1, +1, -1, 0.0, 1.0),
        ],
        [
            (-1, +1, -1, 0.0, 0.0),
            (+1, +1, +1, 1.0, 1.0),
            (+1, +1, -1, 0.0, 1.0),
        ],
        [
            (+1, +1, -1, 0.0, 0.0),
            (+1, -1, +1, 1.0, 1.0),
            (+1, -1, -1, 0.0, 1.0),
        ],
        [
            (+1, -1, -1, 0.0, 0.0),
            (-1, -1, +1, 1.0, 1.0),
            (-1, -1, -1, 0.0, 1.0),
        ],
        [
            (-1, +1, -1, 0.0, 0.0),
            (+1, -1, -1, 1.0, 1.0),
            (-1, -1, -1, 0.0, 1.0),
        ],
        [
            (+1, +1, +1, 0.0, 0.0),
            (-1, -1, +1, 1.0, 1.0),
            (+1, -1, +1, 0.0, 1.0),
        ],
        [
            (-1, -1, -1, 0.0, 0.0),
            (-1, -1, +1, 1.0, 0.0),
            (-1, +1, +1, 1.0, 1.0),
        ],
        [
            (-1, +1, -1, 0.0, 0.0),
            (-1, +1, +1, 1.0, 0.0),
            (+1, +1, +1, 1.0, 1.0),
        ],
        [
            (+1, +1, -1, 0.0, 0.0),
            (+1, +1, +1, 1.0, 0.0),
            (+1, -1, +1, 1.0, 1.0),
        ],
        [
            (+1, -1, -1, 0.0, 0.0),
            (+1, -1, +1, 1.0, 0.0),
            (-1, -1, +1, 1.0, 1.0),
        ],
        [
            (-1, +1, -1, 0.0, 0.0),
            (+1, +1, -1, 1.0, 0.0),
            (+1, -1, -1, 1.0, 1.0),
        ],
        [
            (+1, +1, +1, 0.0, 0.0),
            (-1, +1, +1, 1.0, 0.0),
            (-1, -1, +1, 1.0, 1.0),
        ],
    ]


    @classmethod
    def build_bbox(cls, root_bone: str, mat: str, bbox_min: Vec, bbox_max: Vec) -> 'Mesh':
        """Construct a mesh for a bounding box."""
        mesh = cls.blank(root_bone)
        [root] = mesh.bones.values()
        links = [(root, 1.0)]

        bbox_min, bbox_max = Vec.bbox(bbox_min, bbox_max)

        for tri_def in cls._BBOX_MESH_DATA:
            tri = Triangle(mat, *[
                Vertex(
                    Vec(
                        bbox_max.x if x > 0 else bbox_min.x,
                        bbox_max.y if y > 0 else bbox_min.y,
                        bbox_max.z if z > 0 else bbox_min.z,
                    ), Vec(x, y, z).norm(),
                    u, v, links.copy()
                )
                for x, y, z, u, v in tri_def
            ])
            mesh.triangles.append(tri)
        return mesh
