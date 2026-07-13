from ..model.branch import Branch


class BranchRepository:
    def __init__(self) -> None:
        self._branch_map: dict[str, Branch] = {}

    def add_branch(self, branch: Branch) -> None:
        self._branch_map[branch.id] = branch

    def get_branch(self, branch_id: str) -> Branch | None:
        return self._branch_map.get(branch_id)
