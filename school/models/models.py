# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
     _name = 'school.student'
     _description = 'The students'

     name = fields.Char(string="Nombre", required=True)
     year = fields.Integer()
     topic_id = fields.Many2many("school.topic")
    # topic_id = fields.Many2one("school.topic")


class topic(models.Model):
     _name = 'school.topic'
     _description = 'The topics'
     name = fields.Char(string="Topic name", required=True)
     studens_ids = fields.Many2many("school.student")

class  course(models.Model):
     _name = 'school.course'
     _description = 'Courses'
     name = fields.Char()

     topics = fields.Many2many("school.topic")
     studens = fields.Many2many("school.student")
     repeaters = fields.Many2many(comodel_name='school.student', # El model en el que es relaciona
                            relation='course_students_repeaters_rel', # (opcional) el nom del la taula en mig
                            column1='course_id', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='student_id')  # (opcional) el nom de la columna de l'altre model.
    # studens = fields.One2many("school.student", "topic_id") # necesita que hi haja un Many2one anteriorment
  #   year = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
