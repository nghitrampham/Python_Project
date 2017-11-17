test = {
  'name': 'Problem 11',
  'points': 3,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing BodyguardAnt parameters
          >>> bodyguard = BodyguardAnt()
          >>> BodyguardAnt.food_cost
          c9452203eb0b0f0bd2454586a6c2fc5c
          # locked
          >>> bodyguard.armor
          20d533d3e06345c8bd7072212867f2d1
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing container attributes
          >>> bodyguard = BodyguardAnt()
          >>> print(bodyguard.ant)
          044ef3c0c6fd739b6260fe6f6cae71dd
          # locked
          >>> bodyguard.container
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> test_ant = Ant()
          >>> test_ant.container
          03456a09f22295a39ca84d133a26f63d
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing contain_ant
          >>> bodyguard = BodyguardAnt()
          >>> bodyguard2 = BodyguardAnt()
          >>> test_ant = Ant()
          >>> test_ant2 = Ant()
          >>> bodyguard.can_contain(bodyguard2)
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> bodyguard.can_contain(test_ant)
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> test_ant.can_contain(bodyguard)
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> bodyguard.contain_ant(test_ant)
          >>> bodyguard.ant is test_ant
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> bodyguard.can_contain(test_ant2)
          03456a09f22295a39ca84d133a26f63d
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> hive, layout = Hive(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> bodyguard = BodyguardAnt()
          >>> bodyguard.action(colony) # Action without contained ant should not error
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # Place bodyguard before thrower
          >>> colony.places["tunnel_0_0"].add_insect(bodyguard)
          >>> colony.places["tunnel_0_0"].add_insect(thrower)
          >>> colony.places["tunnel_0_3"].add_insect(bee)
          >>> bodyguard.action(colony)
          >>> bee.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # Place thrower before bodyguard
          >>> colony.places["tunnel_0_0"].add_insect(thrower)
          >>> colony.places["tunnel_0_0"].add_insect(bodyguard)
          >>> colony.places["tunnel_0_3"].add_insect(bee)
          >>> bodyguard.action(colony)
          >>> bee.armor
          1
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> hive, layout = Hive(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
