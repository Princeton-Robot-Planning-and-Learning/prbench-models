"""Tests for the PDDL planning module in prpl_utils."""

from prpl_utils.pddl_planning import run_pyperplan_planning
from relational_structs import (
    GroundAtom,
    LiftedAtom,
    LiftedOperator,
    Object,
    PDDLDomain,
    PDDLProblem,
    Predicate,
    Type,
    Variable,
)


def test_run_pyperplan_planning():
    """Test the run_pyperplan_planning function with a simple PDDL domain and
    problem."""
    # Define types
    object_type = Type(name="object")
    # NOTE: This will have bug
    # block_type = Type(name="block")
    # NOTE: This will not have bug
    block_type = Type(name="block", parent=object_type)

    level1_block_type = Type(name="a_block", parent=block_type)
    level2_block_type = Type(name="b_block", parent=level1_block_type)

    # Define predicates
    On = Predicate(name="On", types=[level1_block_type, level2_block_type])

    # Define objects
    a = Variable(name="?b1", type=level1_block_type)
    b = Variable(name="?b2", type=level2_block_type)

    # Define operators
    pick_place_op = LiftedOperator(
        name="PickPlace",
        parameters=[a, b],
        preconditions=set(),
        add_effects={LiftedAtom(On, [a, b])},
        delete_effects=set(),
    )

    # Define domain
    domain = PDDLDomain(
        name="blocks_world",
        types={object_type, block_type, level1_block_type, level2_block_type},
        predicates={On},
        operators={pick_place_op},
    )

    # Define initial state and goal
    block0 = Object(name="block0", type=level1_block_type)
    block1 = Object(name="block1", type=level2_block_type)

    init_atoms = {}
    goal = {GroundAtom(On, [block0, block1])}

    # Define problem
    problem = PDDLProblem(
        domain_name="blocks_world",
        problem_name="simple_problem",
        objects={block0, block1},
        init_atoms=init_atoms,
        goal=goal,
    )

    # Run planning
    _plan = run_pyperplan_planning(str(domain), str(problem))
