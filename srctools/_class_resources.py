"""For each entity class, specify hardcoded resources.

Those are ones that don't simply appear in fgd.
"""
from typing import Iterator, Callable, Tuple, Union, List, Dict

from srctools.packlist import FileType
from srctools import Entity, conv_int

__all__ = ['CLASS_RESOURCES']

#  For various entity classes, we know they require hardcoded files.
# List them here - classname -> [(file, type), ...]
# Alternatively it's a function to call with the entity to do class-specific
# behaviour, yielding files to pack.

ClassFunc = Callable[[Entity], Iterator[str]]
_cls_res_type = Dict[str, Union[
    ClassFunc,
    List[Union[str, Tuple[str, FileType]],
]]]
CLASS_RESOURCES = {}  # type: _cls_res_type


def res(cls: str, *items: Union[str, Tuple[str, FileType]]):
    """Add a resource to class_resources."""
    CLASS_RESOURCES[cls] = list(items)


def cls_func(func: ClassFunc) -> ClassFunc:
    """Save a function to do special checks for a classname."""
    CLASS_RESOURCES[func.__name__] = func
    return func


# *** Base entities  / HL2 ***
res('env_screeneffect',
    'materials/effects/stun.vmt',
    'materials/effects/introblur.vmt',
    )

res('env_fire_trail',
    'materials/sprites/flamelet1.vmt',
    'materials/sprites/flamelet2.vmt',
    'materials/sprites/flamelet3.vmt',
    'materials/sprites/flamelet4.vmt',
    'materials/sprites/flamelet5.vmt',
    'materials/particle/particle_smokegrenade.vmt',
    'materials/particle/particle_noisesphere.vmt',
    )

res('env_steam',
    'materials/particle/particle_smokegrenade.vmt',
    'materials/sprites/heatwave.vmt',
)
CLASS_RESOURCES['env_steamjet'] = CLASS_RESOURCES['env_steam']

res('env_starfield',
    'materials/effects/spark_noz.vmt',
    )

res('func_dust',
    'materials/particle/sparkles.vmt',
    )

res('func_tankchange',
    ('FuncTrackChange.Blocking', FileType.GAME_SOUND),
    )

res('npc_combine_cannon',
    'models/combine_soldier.mdl',
    'materials/effects/bluelaser1.vmt',
    'materials/sprites/light_glow03.vmt',
    ('NPC_Combine_Cannon.FireBullet', FileType.GAME_SOUND),
)


@cls_func
def func_breakable_surf(ent: Entity):
    """Additional materials required for func_breakable_surf."""
    yield 'models/brokenglass_piece.mdl'

    surf_type = conv_int(ent['surfacetype'])
    if surf_type == 1:  # Tile
        yield from (
            'materials/models/brokentile/tilebroken_03a.vmt',
            'materials/models/brokentile/tilebroken_03b.vmt',
            'materials/models/brokentile/tilebroken_03c.vmt',
            'materials/models/brokentile/tilebroken_03d.vmt',

            'materials/models/brokentile/tilebroken_02a.vmt',
            'materials/models/brokentile/tilebroken_02b.vmt',
            'materials/models/brokentile/tilebroken_02c.vmt',
            'materials/models/brokentile/tilebroken_02d.vmt',

            'materials/models/brokentile/tilebroken_01a.vmt',
            'materials/models/brokentile/tilebroken_01b.vmt',
            'materials/models/brokentile/tilebroken_01c.vmt',
            'materials/models/brokentile/tilebroken_01d.vmt',
        )
    elif surf_type == 0:  # Glass
        yield from (
            'materials/models/brokenglass/glassbroken_solid.vmt',
            'materials/models/brokenglass/glassbroken_01a.vmt',
            'materials/models/brokenglass/glassbroken_01b.vmt',
            'materials/models/brokenglass/glassbroken_01c.vmt',
            'materials/models/brokenglass/glassbroken_01d.vmt',
            'materials/models/brokenglass/glassbroken_02a.vmt',
            'materials/models/brokenglass/glassbroken_02b.vmt',
            'materials/models/brokenglass/glassbroken_02c.vmt',
            'materials/models/brokenglass/glassbroken_02d.vmt',
            'materials/models/brokenglass/glassbroken_03a.vmt',
            'materials/models/brokenglass/glassbroken_03b.vmt',
            'materials/models/brokenglass/glassbroken_03c.vmt',
            'materials/models/brokenglass/glassbroken_03d.vmt',
        )


@cls_func
def move_rope(ent: Entity):
    """Implement move_rope and keyframe_rope resources."""
    old_shader_type = conv_int(ent['RopeShader'])
    if old_shader_type == 0:
        yield 'materials/cable/cable.vmt'
    elif old_shader_type == 1:
        yield 'materials/cable/rope.vmt'
    else:
        yield 'materials/cable/chain.vmt'
    yield 'materials/cable/rope_shadowdepth.vmt'

# These classes are identical.
CLASS_RESOURCES['keyframe_rope'] = CLASS_RESOURCES['move_rope']


res('npc_vehicledriver',
    'models/roller_vehicledriver.mdl',
    )

res('point_spotlight',
    'materials/sprites/light_glow03.vmt',
    'materials/sprites/glow_test02.vmt',
    )

res('vgui_screen',
    'materials/engine/writez.vmt',
    )

# *** Portal 1/2 ***

res('point_energy_ball_launcher',
    'models/effects/combineball.mdl',
    'materials/effects/eball_finite_life.vmt',
    'materials/effects/eball_infinite_life.vmt',

    'sound/weapons/physcannon/energy_bounce1.wav',
    'sound/weapons/physcannon/energy_bounce2.wav',
    'sound/weapons/physcannon/energy_disintegrate4.wav',
    'sound/weapons/physcannon/energy_disintegrate5.wav',
    'sound/weapons/physcannon/energy_sing_explosion2.wav',
    'sound/weapons/physcannon/energy_sing_flyby1.wav',
    'sound/weapons/physcannon/energy_sing_flyby2.wav',
    'sound/weapons/physcannon/energy_sing_loop4.wav',
    )

res('prop_button',
    'models/props/switch001.mdl'
    )

CLASS_RESOURCES['prop_energy_ball'] = CLASS_RESOURCES['point_energy_ball_launcher']


# *** Team Fortress 2 ***

@cls_func
def item_teamflag(ent: Entity) -> Iterator[str]:
    """This item has several special team-specific options."""
    for kvalue, prefix in [
        ('flag_icon', 'materials/vgui/'),
        ('flag_trail', 'materials/effects/')
    ]:
        value = prefix +ent[kvalue]
        if value != prefix:
            yield value + '.vmt'
            yield value + '_red.vmt'
            yield value + '_blue.vmt'

@cls_func
def team_control_point(ent: Entity) -> Iterator[str]:
    """Special '_locked' materials."""
    for kvalue in ['team_icon_0', 'team_icon_1', 'team_icon_2']:
        mat = ent[kvalue]
        if mat:
            yield 'materials/{}.vmt'.format(mat)
            yield 'materials/{}_locked.vmt'.format(mat)
