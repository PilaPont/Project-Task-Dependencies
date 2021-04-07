# Copyright 2016-2020 Onestein (<http://www.onestein.eu>)
# Copyright 2020 Tecnativa - Manuel Calero
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import itertools
from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    required_task_ids = fields.One2many(comodel_name='task.dependency', inverse_name='dependent_task_id')
    dependent_task_ids = fields.One2many(comodel_name='task.dependency', inverse_name='required_task_id')

    @api.constrains("required_task_ids", "dependent_task_ids")
    def _check_dependency_recursion(self):

        self.flush(['required_task_ids', 'dependent_task_ids'])
        cr = self._cr
        query = r'SELECT dependent_task_id,required_task_id FROM task_dependency WHERE dependent_task_id IN %s'
        successors = defaultdict(set)  # transitive closure of successors
        predecessors = defaultdict(set)  # transitive closure of predecessors
        todo, done = set(self.ids), set()
        while todo:
            # retrieve the respective successors of the nodes in 'todo'
            cr.execute(query, [tuple(todo)])
            done.update(todo)
            todo.clear()
            for id1, id2 in cr.fetchall():
                # connect id1 and its predecessors to id2 and its successors
                for x, y in itertools.product([id1] + list(predecessors[id1]),
                                              [id2] + list(successors[id2])):
                    if x == y:
                        # we found a cycle here!
                        raise ValidationError(
                            _("You cannot create recursive dependencies between tasks. %s conflicts") % self.browse(
                                [x]).name)

                    successors[x].add(y)
                    predecessors[y].add(x)
                if id2 not in done:
                    todo.add(id2)

    def copy(self, default=None):
        res = super().copy(default)
        if self.env.context.get("project_copy"):
            self.env["project.task.copy.map"].create(
                {"old_task_id": self.id, "new_task_id": res.id}
            )
        else:
            for task_dependency in self.required_task_ids:
                task_dependency.copy({'dependent_task_id': res.id})
        return res
