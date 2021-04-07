from odoo import api, fields, models


class TaskDependency(models.Model):
    _name = 'task.dependency'
    _description = 'Task Dependency'

    dependent_task_id = fields.Many2one(comodel_name="project.task", index=False, required=True)
    required_task_id = fields.Many2one(comodel_name="project.task", required=True)
    relation_type = fields.Selection([
        ('start_to_start', 'Start to Start'),
        ('start_to_end', 'Start to End'),
        ('end_to_start', 'End to Start'),
        ('end_to_end', 'End to End')
    ], required=True, default='end_to_start')
    project_id = fields.Many2one(comodel_name='project.project', compute='_compute_project_id')

    _sql_constraints = [
        ('dependency_task_uniq', 'unique (dependent_task_id,required_task_id )', "Duplicate dependency found."),
    ]

    @api.depends('dependent_task_id', 'required_task_id')
    def _compute_project_id(self):
        for dependency in self:
            dependency.project_id = dependency.dependent_task_id.project_id or dependency.required_task_id.project_id
