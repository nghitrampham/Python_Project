test = {
  'name': 'Problem 10',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing HungryAnt parameters
          >>> hungry = HungryAnt()
          >>> HungryAnt.food_cost
          c9452203eb0b0f0bd2454586a6c2fc5c
          # locked
          >>> hungry.armor
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # Testing HungryAnt eats and digests
          >>> hungry = HungryAnt()
          >>> super_bee, wimpy_bee = Bee(1000), Bee(1)
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> place.add_insect(super_bee)
          >>> hungry.action(colony)         # super_bee is no match for HungryAnt!
          >>> super_bee.armor
          73b94a1326ae2e803c3421016112207b
          # locked
          >>> place.add_insect(wimpy_bee)
          >>> for _ in range(3):
          ...     hungry.action(colony)     # digesting...not eating
          >>> wimpy_bee.armor
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> hungry.action(colony)         # back to eating!
          >>> wimpy_bee.armor
          73b94a1326ae2e803c3421016112207b
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
    }
  ]
}
