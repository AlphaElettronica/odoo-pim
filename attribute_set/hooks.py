# Copyright 2023 ForgeFlow S.L.  <https://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.base_sparse_field.models.models import IrModelFields
from odoo.fields import Field


def post_load_hook():
    def _instanciate_attrs(self, field_data):
        attrs = super(IrModelFields, self)._instanciate_attrs(field_data)
        if attrs and field_data.get("serialization_field_id"):
            serialization_record_id = field_data["serialization_field_id"]
            try:
                serialization_record = self.browse(serialization_record_id)
                attrs["sparse"] = serialization_record.name
            except AttributeError:
                # due to https://github.com/OCA/odoo-pim/issues/134
                # because depends_context isn't filled yet
                attrs["sparse"] = None
        return attrs

    # per come sono costruiti i field di odoo 12.0, è necessario fare l'override
    # anche della __getattr__ di Field, poichè _attrs può non essere definito
    # all'inizializzazione dell'istanza del Field.
    def attrs_getattr(self, name):
        if name == '_attrs':
            return {}
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    IrModelFields._instanciate_attrs = _instanciate_attrs
    Field.__getattr__ = attrs_getattr
