from odoo import models


class ProjectProject(models.Model):
    _inherit = "project.project"

    def copy(self, default=None):
        self.ensure_one()
        res = super(ProjectProject, self.with_context(project_copy=True)).copy(default)

        mappings = self.env["project.task.copy.map"].search(
            [("new_task_id.project_id", "=", res.id)]
        )
        for task in res.tasks:
            mapping = mappings.filtered(lambda m: m.new_task_id.id == task.id)
            for task_dependency in mapping.old_task_id.required_task_ids:
                new_required_task_id = mappings.filtered(
                    lambda m: m.old_task_id.id == task_dependency.required_task_id.id).new_task_id
                task_dependency.copy(
                    {'dependent_task_id': mapping.new_task_id.id, 'required_task_id': new_required_task_id.id})

        return res
