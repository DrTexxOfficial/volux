import pytest
import volux
from voluxcliprint import VoluxCliPrint

# create Volux Operator object (hub for communication between modules)
vlx = volux.VoluxOperator()
volux_module_cli_print = VoluxCliPrint()

class Test_voluxcliprint:
    def test_adding_module(self):
        vlx.add_module(volux_module_cli_print)
        assert volux_module_cli_print in vlx.modules

    def test_get_modules(self):
        print(vlx.get_modules())
        assert vlx.get_modules() == vlx.modules

    def test_set_value(self):
        vlx.demo.set(20)
        assert vlx.demo.get() == 20

    def test_set_nonsense(self):
        with pytest.raises(TypeError):
            vlx.demo.set('2') # number as string
