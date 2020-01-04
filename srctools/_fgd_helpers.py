"""Implemenations of specific code for each FGD helper type."""
from typing import (
    List, Optional, Iterator, Union, Tuple, TYPE_CHECKING,
    Collection,
)

from srctools import Vec, parse_vec_str
from srctools.fgd import HelperTypes, Helper

if TYPE_CHECKING:
    from srctools.fgd import EntityDef


__all__ = [
    'HelperBBox', 'HelperBoundingBox', 'HelperBreakableSurf',
    'HelperBrushSides', 'HelperCylinder', 'HelperDecal',
    'HelperEnvSprite', 'HelperFrustum', 'HelperHalfGridSnap',
    'HelperInherit', 'HelperInstance', 'HelperLight', 'HelperLightSpot',
    'HelperLine', 'HelperModel', 'HelperModelLight', 'HelperModelProp',
    'HelperOrientedBBox', 'HelperOrigin', 'HelperOverlay',
    'HelperOverlayTransition', 'HelperRenderColor', 'HelperRope',
    'HelperSize', 'HelperSphere', 'HelperSprite',
    'HelperSweptPlayerHull', 'HelperTrack', 'HelperTypes',
    'HelperVecLine', 'HelperWorldText',

    'HelperExtAppliesTo', 'HelperExtAutoVisgroups', 'HelperExtOrderBy',
]


class _HelperOneOptional(Helper):
    """Utility base class for a helper with one optional parameter."""
    _DEFAULT = None  # type: str

    def __init__(self, key: str) -> None:
        self.key = key

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse a single optional keyl."""
        if len(args) > 1:
            raise ValueError(
                'Expected up to 1 argument, got ({})!'.format(', '.join(args))
            )
        elif len(args) == 1:
            key = args[0]
        else:
            key = cls._DEFAULT
        return cls(key)

    def export(self) -> List[str]:
        """Export the helper.

        If the key is the default it is omitted.
        """
        if self.key == self._DEFAULT:
            return []
        else:
            return [self.key]


class HelperInherit(Helper):
    """Helper implementation for base().

    These specify the base classes for an entity def.
    This implementation isn't used, the EntityDef special-cases it.
    """
    TYPE = HelperTypes.INHERIT


class HelperHalfGridSnap(Helper):
    """Helper implementation for halfgridsnap().

    This causes the entity to snap to half a grid.
    This argument doesn't use () in Valve's files.
    """
    TYPE = HelperTypes.HALF_GRID_SNAP


class HelperSize(Helper):
    """Helper implementation for size().

    This sets the bbox for the entity.
    """
    TYPE = HelperTypes.CUBE

    def __init__(self, point1: Vec, point2: Vec) -> None:
        self.bbox_min, self.bbox_max = Vec.bbox(point1, point2)

    def overrides(self) -> Collection[HelperTypes]:
        """Additional versions of this are not available."""
        return [HelperTypes.CUBE]

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse size(x1 y1 z1, x2 y2 z2)."""
        if len(args) > 2:
            raise ValueError(
                'Expected 1 or 2 arguments, got ({})!'.format(', '.join(args))
            )
        size_min = Vec.from_str(args[0])
        if len(args) == 2:
            size_max = Vec.from_str(args[1])
        else:
            # "min" is actually the dimensions.
            size_max = size_min / 2
            size_min = -size_max

        return cls(size_min, size_max)

    def export(self) -> List[str]:
        """Produce (x1 y1 z1, x2 y2 z2)."""
        return [
            str(self.bbox_min),
            str(self.bbox_max),
        ]


class HelperBBox(HelperSize):
    """Helper implementation for bbox()."""
    TYPE = HelperTypes.BBOX


class HelperRenderColor(Helper):
    """Helper implementation for color()."""
    TYPE = HelperTypes.TINT

    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b

    def overrides(self) -> Collection[HelperTypes]:
        """Previous ones of these are overridden by this."""
        return [HelperTypes.TINT]

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse color(R G B)."""
        try:
            [tint] = args
        except ValueError:
            raise ValueError(
                'Expected 1 argument, got ({})!'.format(', '.join(args))
            ) from None

        r, g, b = parse_vec_str(tint)

        return cls(r, g, b)

    def export(self) -> List[str]:
        """Produce color(R G B)."""
        return ['{:g} {:g} {:g}'.format(self.r, self.g, self.b)]


class HelperSphere(Helper):
    """Helper implementation for sphere()."""
    TYPE = HelperTypes.SPHERE
    def __init__(self,  r: float, g: float, b: float,  size_key: str) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.size_key = size_key

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse sphere(radius, r g b)."""
        arg_count = len(args)
        if arg_count > 2:
            raise ValueError(
                'Expected 1 or 2 arguments, got ({})!'.format(', '.join(args))
            )
        r = g = b = 255

        if arg_count > 0:
            size_key = args[0]
            if arg_count == 2:
                r, g, b = parse_vec_str(args[1])
        else:
            size_key = 'radius'

        return cls(r, g, b, size_key)

    def export(self) -> List[str]:
        """Export the helper.

        If the key is the default it is omitted.
        """
        if self.r != 255.0 or self.g != 255.0 or self.b != 255.0:
            return [
                # Even if "radius", we need to pass the arg to allow color.
                self.size_key,
                '{:g} {:g} {:g}'.format(self.r, self.g, self.b)
            ]
        elif self.size_key != 'radius':
            return [self.size_key]
        else:
            return []


class HelperLine(Helper):
    """Helper implementation for line().

    Line has the arguments line(r g b, start_key, start_value, end_key, end_value)
    It searches for the first entity where ent[start_key] == self[start_value].
    If the second pair are present it does the same for those for the other
    line end.
    """
    TYPE = HelperTypes.LINE

    def __init__(
        self,
        r: float, g: float, b: float,
        start_key: str,
        start_value: str,
        end_key: Optional[str]=None,
        end_value: Optional[str]=None,
    ) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.start_key = start_key
        self.start_value = start_value
        if end_key is not None and end_value is not None:
            self.end_key = end_key
            self.end_value = end_value
        else:
            self.end_key = self.end_value = None

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse line(r g b, start_key, start_value, end_key, end_value)."""
        arg_count = len(args)
        if arg_count not in (3, 5):
            raise ValueError(
                'Expected 3 or 5 arguments, got ({})!'.format(
                    ', '.join(args))
            ) from None

        r, g, b = parse_vec_str(args[0])
        start_key = args[1]
        start_value = args[2]

        if arg_count == 5:
            end_key = args[3]
            end_value = args[4]
        else:
            end_key = end_value = None

        return cls(r, g, b, start_key, start_value, end_key, end_value)

    def export(self) -> List[str]:
        """Produce the correct line() arguments."""
        args = [
            '{:g} {:g} {:g}'.format(self.r, self.g, self.b),
            self.start_key,
            self.start_value,
        ]
        if self.end_key is not None and self.end_value is not None:
            args += [self.end_key, self.end_value]
        return args


class HelperFrustum(Helper):
    """Helper for env_projectedtexture visuals."""
    TYPE = HelperTypes.FRUSTUM

    def __init__(
        self,
        fov: Union[str, float],
        near: Union[str, float],
        far: Union[str, float],
        color: Union[str, Tuple[float, float, float]],
        pitch_scale: Union[str, float],
    ) -> None:
        self.fov = fov
        self.near_z = near
        self.far_z = far
        self.color = color
        self.pitch_scale = pitch_scale

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse frustum(fov, near, far, color, pitch_scale)."""
        # These are the default values if not provided.
        fov = '_fov'
        nearz = '_nearplane'
        farz = '_farz'
        color = '_light'
        pitch = -1.0

        try:
            fov = args[0]
            nearz = args[1]
            farz = args[2]
            color = args[3]
            pitch = args[4]
        except IndexError:
            pass  # Stop once out of args.
        else:
            if len(args) > 5:
                raise ValueError(
                    'Expected at most 5 arguments, '
                    'got ({})!'.format(', '.join(args))
                )

        # Try and parse everything, but if it fails ignore since they could
        # be property names.
        try:
            fov = float(fov)
        except ValueError:
            pass
        try:
            nearz = float(nearz)
        except ValueError:
            pass
        try:
            farz = float(farz)
        except ValueError:
            pass
        try:
            pitch = float(pitch)
        except ValueError:
            pass

        try:
            r, g, b = color.split()
            color = (float(r), float(g), float(b))
        except ValueError:
            pass

        return cls(fov, nearz, farz, color, pitch)

    def export(self) -> List[str]:
        """Export back out frustrum() arguments."""

        if isinstance(self.color, tuple):
            color = '{:g} {:g} {:g}'.format(*self.color)
        else:
            color = self.color

        def conv(x: 'Union[str, float]') -> str:
            """Ensure the .0 is removed from the float forms. """
            return format(x, 'g') if isinstance(x, float) else x

        return [
            conv(self.fov),
            conv(self.near_z),
            conv(self.far_z),
            color,
            conv(self.pitch_scale),
        ]


class HelperCylinder(HelperLine):
    """Helper implementation for cylinder().

    Cylinder has the same sort of arguments as line(), plus radii for both positions.
    """
    TYPE = HelperTypes.CYLINDER

    def __init__(
        self,
        r: float, g: float, b: float,
        start_key: str,
        start_value: str,
        start_radius: str,
        end_key: Optional[str]=None,
        end_value: Optional[str]=None,
        end_radius: Optional[str]=None,
    ) -> None:
        super().__init__(r, g, b, start_key, start_value, end_key, end_value)
        self.start_radius = start_radius
        self.end_radius = end_radius if self.end_key is not None else None

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse cylinder(r g b, start key/value/radius, end key/value/radius)."""
        arg_count = len(args)
        if arg_count not in (3, 4, 6, 7):
            raise ValueError(
                'Expected 3, 4, 6 or 7 arguments, got ({})!'.format(
                    ', '.join(args))
            ) from None

        r, g, b = parse_vec_str(args[0])
        start_key = args[1]
        start_value = args[2]

        start_radius = end_key = end_value = end_radius = None
        if arg_count > 3:
            start_radius = args[3]
            if arg_count >= 6:
                end_key = args[4]
                end_value = args[5]
                if arg_count == 7:
                    end_radius = args[6]

        return cls(
            r, g, b,
            start_key, start_value, start_radius,
            end_key, end_value, end_radius,
        )

    def export(self) -> List[str]:
        """Produce the correct line() arguments."""
        args = [
            '{:g} {:g} {:g}'.format(self.r, self.g, self.b),
            self.start_key,
            self.start_value,
        ]
        if self.start_radius is not None:
            args.append(self.start_radius)
            if self.end_key is not None and self.end_value is not None:
                args += [self.end_key, self.end_value]
                if self.end_radius is not None:
                    args.append(self.end_radius)
        return args


class HelperOrigin(_HelperOneOptional):
    """Parse the origin() helper."""
    TYPE = HelperTypes.ORIGIN
    _DEFAULT = 'origin'


class HelperVecLine(_HelperOneOptional):
    """A variant of line() which draws a line to the entity."""
    TYPE = HelperTypes.VECLINE
    _DEFAULT = 'origin'


class HelperBrushSides(_HelperOneOptional):
    """Highlights brush faces in a space-sepearated keyvalue."""
    TYPE = HelperTypes.BRUSH_SIDES
    _DEFAULT = 'sides'


class HelperBoundingBox(Helper):
    """Displays bounding box between two keyvalues."""
    TYPE = HelperTypes.BOUNDING_BOX_HELPER

    def __init__(self, key_min: str, key_max: str) -> None:
        self.min = key_min
        self.max = key_max

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse wirebox(min, max)"""
        try:
            [key_min, key_max] = args
        except ValueError:
            raise ValueError(
                'Expected 2 arguments, got ({})!'.format(', '.join(args))
            ) from None

        return cls(key_min, key_max)

    def export(self) -> List[str]:
        """Produce the wirebox(min, max) arguments."""
        return [self.min, self.max]


class HelperSweptPlayerHull(Helper):
    """Draws the movement of a player-sized bounding box from A to B."""
    TYPE = HelperTypes.SWEPT_HULL


class HelperOrientedBBox(HelperBoundingBox):
    """A bounding box oriented to angles."""
    TYPE = HelperTypes.ORIENTED_BBOX


class HelperSprite(Helper):
    """The sprite helper, for editor icons.

    If the material is not provided, the 'model' key is used.
    """
    TYPE = HelperTypes.SPRITE

    def __init__(self, material: Optional[str]):
        self.mat = material

    def overrides(self) -> Collection[HelperTypes]:
        if self.mat is None:
            return ()  # When not set, this doesn't affect anything.
        else:
            # This doesn't override either of these,
            # but if you have two sprites it's pointless.
            # And so is a box + sprite.
            return [HelperTypes.CUBE, HelperTypes.SPRITE, HelperTypes.ENT_SPRITE]

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse iconsprite(mat)."""
        if len(args) > 1:
            raise ValueError(
                'Expected up to 1 argument, got ({})!'.format(', '.join(args))
            )
        elif len(args) == 1:
            return cls(args[0])
        else:
            return cls(None)

    def export(self) -> List[str]:
        """Produce the arguments for iconsprite()."""
        if self.mat is not None:
            return [self.mat]
        else:
            return []

    def get_resources(self, entity: 'EntityDef') -> Iterator[str]:
        """iconsprite() uses a single material."""
        if self.mat is None:
            try:
                materials = entity.kv['model'].known_options()
            except KeyError:
                return
        else:
            materials = [self.mat]

        for material in materials:
            material = material.replace('\\', '/')

            if not material.casefold().endswith('.vmt'):
                material += '.vmt'
            if not material.casefold().startswith('materials/'):
                material = 'materials/' + material

            yield material


class HelperEnvSprite(HelperSprite):
    """Variant of iconsprite() specifically for env_sprite."""
    TYPE = HelperTypes.ENT_SPRITE


class HelperModel(Helper):
    """Helper which displays models.

    If the model is not provided, the 'model' key is used.
    """
    TYPE = HelperTypes.MODEL

    def __init__(self, model: Optional[str]):
        self.model = model

    def overrides(self) -> Collection[HelperTypes]:
        if self.model is None:
            return ()  # When not set, this doesn't affect anything.
        else:
            return [HelperTypes.CUBE]

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        """Parse iconsprite(mat)."""
        if len(args) > 1:
            raise ValueError(
                'Expected up to 1 argument, got ({})!'.format(', '.join(args))
            )
        elif len(args) == 1:
            return cls(args[0])
        else:
            return cls(None)

    def export(self) -> List[str]:
        """Produce the arguments for iconsprite()."""
        if self.model is not None:
            return [self.model]
        else:
            return []

    def get_resources(self, entity: 'EntityDef') -> Iterator[str]:
        """studio() uses a single material."""
        if self.model is None:
            try:
                models = entity.kv['model'].known_options()
            except KeyError:
                return
        else:
            models = [self.model]

        for mdl in models:
            mdl = mdl.replace('\\', '/')

            if not mdl.casefold().endswith('.mdl'):
                mdl += '.mdl'
            if not mdl.casefold().startswith('models/'):
                mdl = 'models/' + mdl

            yield mdl


class HelperModelProp(HelperModel):
    """Model helper which does not affect the bounding box."""
    TYPE = HelperTypes.MODEL_PROP


# These are all specialised for a particular entity.
# There's rarely options available.


class HelperModelLight(HelperModel):
    """Special model helper, with inverted pitch."""
    TYPE = HelperTypes.MODEL_NEG_PITCH



class HelperInstance(Helper):
    """Specialized helper for func_instance."""
    TYPE = HelperTypes.ENT_INSTANCE


class HelperDecal(Helper):
    """Specialized helper for infodecal."""
    TYPE = HelperTypes.ENT_DECAL


class HelperOverlay(Helper):
    """Specialized helper for env_overlay."""
    TYPE = HelperTypes.ENT_OVERLAY


class HelperOverlayTransition(Helper):
    """Specialized helper for env_overlay_transition."""
    TYPE = HelperTypes.ENT_OVERLAY_WATER


class HelperLight(Helper):
    """Specialized helper for omnidirectional lights."""
    TYPE = HelperTypes.ENT_LIGHT


class HelperLightSpot(Helper):
    """Specialized helper for displaying spotlight previews."""
    TYPE = HelperTypes.ENT_LIGHT_CONE


class HelperRope(Helper):
    """Specialized helper for displaying move_rope and keyframe_rope."""
    TYPE = HelperTypes.ENT_ROPE


class HelperTrack(Helper):
    """Specialized helper for path_track-style entities.

    This no longer does anything.
    """
    TYPE = HelperTypes.ENT_TRACK


class HelperBreakableSurf(Helper):
    """Specialized helper for func_breakable_surf."""
    TYPE = HelperTypes.ENT_BREAKABLE_SURF


class HelperWorldText(Helper):
    """Specialized helper for point_worldtext."""
    TYPE = HelperTypes.ENT_WORLDTEXT


# Extensions to the FGD format.

class HelperExtAppliesTo(Helper):
    """Allows specifying "tags" to indicate an entity is only used in certain games."""
    TYPE = HelperTypes.EXT_APPLIES_TO
    IS_EXTENSION = True

    def __init__(self, tags: List[str]):
        self.tags = tags

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        return cls(args)

    def export(self) -> List[str]:
        return self.tags


class HelperExtOrderBy(Helper):
    """Reorder keyvalues. Args = names in order."""
    TYPE = HelperTypes.EXT_ORDERBY
    IS_EXTENSION = True

    def __init__(self, order: List[str]):
        self.order = order

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        return cls(args)

    def export(self) -> List[str]:
        return self.order


class HelperExtAutoVisgroups(Helper):
    """Convenience for parsing, adds @AutoVisgroups to entities.

    'Auto' is implied at the start."""
    TYPE = HelperTypes.EXT_AUTO_VISGROUP
    IS_EXTENSION = True

    def __init__(self, path: List[str]) -> None:
        self.path = path

    @classmethod
    def parse(cls, args: List[str]) -> 'Helper':
        if len(args) > 0 and args[0].casefold() != 'auto':
            args.insert(0, 'Auto')
        if len(args) < 2:
            raise ValueError('Expected requires 2 or more arguments, got {}!')
        return cls(args)

    def export(self) -> List[str]:
        return self.path

