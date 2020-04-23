from PyQt5.QtCore import Qt

__all__ = ['FormModel']


class FormModel:
    @property
    def model(self):
        raise NotImplementedError("Model is not implemented")

    def _connect_model(self, model):
        for attr, elem in model['line'].items():
            self._line_edit_model(attr, elem)

        for attr, elem in model['checkbox'].items():
            self._checkbox_model(attr, elem)

        for attr, elem in model['combobox'].items():
            self._combobox_model(attr, elem)

    def _line_edit_model(self, attr, elem):
        def on_text_changed(text):
            if text == '':
                setattr(self.model, attr, None)
            else:
                setattr(self.model, attr, text)

        elem = getattr(self.ui, elem)
        elem.setText(getattr(self.model, attr))
        elem.textEdited.connect(on_text_changed)

    def _checkbox_model(self, attr, elem):
        def on_state_changed(state):
            setattr(self.model, attr, state != 0)

        elem = getattr(self.ui, elem)
        if getattr(self.model, attr):
            elem.setCheckState(Qt.Checked)
        else:
            elem.setCheckState(Qt.Unchecked)

        elem.stateChanged.connect(on_state_changed)

    def _combobox_model(self, attr, elem):
        cast = type(getattr(self.model, attr))

        def on_current_text_changed(text):
            setattr(self.model, attr, cast(text))

        elem = getattr(self.ui, elem)
        elem.setCurrentText(str(getattr(self.model, attr)))
        elem.currentTextChanged.connect(on_current_text_changed)
