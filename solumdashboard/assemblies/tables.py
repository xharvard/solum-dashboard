# Copyright (c) 2014 Rackspace Hosting.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.utils.translation import ugettext as _

from horizon import tables

from solumdashboard.api.client import client as solumclient


class CreateAssembly(tables.LinkAction):
    name = "create"
    verbose_name = _("New Assembly")
    url = "horizon:solum:assemblies:create"
    classes = ("btn-launch", "ajax-modal")


class DeleteAssembly(tables.BatchAction):
    name = "delete"
    verbose_name = _("Delete Assembly")
    classes = ("btn-terminate", "btn-danger")

    action_present = _("Delete")
    action_past = _("Deleted")
    data_type_singular = _("Assembly")
    data_type_plural = _("Assemblies")

    def allowed(self, request, template):
        return True

    def action(self, request, assembly_id):
        solum = solumclient(request)
        solum.assemblies.delete(assembly_id=assembly_id)


class ViewAssembly(tables.LinkAction):
    name = "view"
    verbose_name = _("View")
    url = "horizon:solum:assemblies:detail"
    classes = ("btn-edit",)


class AssembliesTable(tables.DataTable):
    uuid = tables.Column('uuid', verbose_name=_('UUID'),
                         link=("horizon:solum:assemblies:detail"))
    name = tables.Column('name', verbose_name=_('Name'))
    application = tables.Column('application', verbose_name=_('Application'),
                                link=("horizon:solum:applications:detail"))
    description = tables.Column('description', verbose_name=_('Description'))

    def get_object_id(self, app):
        return app.uuid

    class Meta:
        name = "assemblies"
        verbose_name = _("Assemblies")
        table_actions = (DeleteAssembly,)
        row_actions = (ViewAssembly, DeleteAssembly)
