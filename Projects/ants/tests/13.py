test = {
  'name': 'Problem 13',
  'points': 3,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing QueenAnt parameters
          >>> ants.QueenAnt.food_cost
          7cd035adf49fc93a635b4e8bb2e28bd4
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # QueenAnt Placement
          >>> queen = ants.QueenAnt()
          >>> impostor = ants.QueenAnt()
          >>> front_ant, back_ant = ants.ThrowerAnt(), ants.ThrowerAnt()
          >>> tunnel = [colony.places['tunnel_0_{0}'.format(i)]
          ...         for i in range(9)]
          >>> tunnel[1].add_insect(back_ant)
          >>> tunnel[7].add_insect(front_ant)
          >>> tunnel[4].add_insect(impostor)
          >>> impostor.action(colony)
          >>> impostor.armor            # Impostors must die!
          73b94a1326ae2e803c3421016112207b
          # locked
          >>> tunnel[4].ant is None
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> back_ant.damage           # Ants should not be buffed
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> front_ant.damage
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> tunnel[4].add_insect(queen)
          >>> queen.action(colony)
          >>> queen.armor               # Long live the Queen!
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> back_ant.damage           # Ants behind queen should be buffed
          20d533d3e06345c8bd7072212867f2d1
          # locked
          >>> front_ant.damage
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> # QueenAnt Removal
          >>> queen = ants.QueenAnt()
          >>> impostor = ants.QueenAnt()
          >>> place = colony.places['tunnel_0_2']
          >>> place.add_insect(impostor)
          >>> place.remove_insect(impostor)
          >>> place.ant is None         # Impostors can be removed
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> place.add_insect(queen)
          >>> place.remove_insect(queen)
          >>> place.ant is queen        # True queen cannot be removed
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': r"""
      >>> import ants, importlib
      >>> importlib.reload(ants)
      >>> hive = ants.Hive(ants.AssaultPlan())
      >>> dimensions = (2, 9)
      >>> colony = ants.AntColony(None, hive, ants.ant_types(),
      ...         ants.dry_layout, dimensions)
      >>> ants.bees_win = lambda: None
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing game over
          >>> queen = ants.QueenAnt()
          >>> impostor = ants.QueenAnt()
          >>> tunnel = [colony.places['tunnel_0_{0}'.format(i)]
          ...         for i in range(9)]
          >>> tunnel[4].add_insect(queen)
          >>> tunnel[6].add_insect(impostor)
          >>> bee = ants.Bee(3)
          >>> tunnel[6].add_insect(bee)     # Bee in place with impostor
          >>> bee.action(colony)            # Game should not end
          
          >>> bee.move_to(tunnel[4])        # Bee moved to place with true queen
          >>> bee.action(colony)            # Game should end
          BeesWinException
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing if queen will not crash with no one to buff
          >>> queen = ants.QueenAnt()
          >>> colony.places['tunnel_0_2'].add_insect(queen)
          >>> queen.action(colony)
          >>> # Attack a bee
          >>> bee = ants.Bee(3)
          >>> colony.places['tunnel_0_4'].add_insect(bee)
          >>> queen.action(colony)
          >>> bee.armor # Queen should still hit the bee
          2
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> import ants, importlib
      >>> importlib.reload(ants)
      >>> hive = ants.Hive(ants.AssaultPlan())
      >>> dimensions = (2, 9)
      >>> colony = ants.AntColony(None, hive, ants.ant_types(),
      ...         ants.dry_layout, dimensions)
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
