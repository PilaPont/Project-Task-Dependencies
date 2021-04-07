from odoo import fields, models


class ProjectTaskCopyMap(models.TransientModel):
    _name = "project.task.copy.map"
    _description = "Project Task Copy Map"

    old_task_id = fields.Many2one(comodel_name="project.task", ondelete="cascade")
    new_task_id = fields.Many2one(comodel_name="project.task", ondelete="cascade")
