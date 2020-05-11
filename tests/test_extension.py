from expanda.extension import Extension
from unittest import mock


@mock.patch('importlib.import_module')
def test_extension_meta_data(mock_import_module):
    module = mock_import_module.return_value
    module.__extension__ = {
        'name': 'Name Field',
        'version': 'Version Field',
        'description': 'Description Field',
        'author': 'Author Field',
        'main': None
    }

    ext = Extension(None)
    assert ext.ext_name == 'Name Field'
    assert ext.version == 'Version Field'
    assert ext.description == 'Description Field'
    assert ext.author == 'Author Field'


@mock.patch('importlib.import_module')
def test_extension_call(mock_import_module):
    module = mock_import_module.return_value

    mock_func = mock.Mock()
    module.__extension__ = {
        'main': mock_func,
        'arguments': {
            'x': {'type': int},
            'y': {'type': float, 'default': 3.14}
        }
    }

    ext = Extension(None)
    ext.call('input_files', 'output_files', 'workspace', {'x': '5'})
    assert mock_func.called

    called_args, _ = mock_func.call_args
    assert called_args[0] == 'input_files'
    assert called_args[1] == 'output_files'
    assert called_args[2] == 'workspace'
    assert called_args[3]['x'] == 5
    assert called_args[3]['y'] == 3.14

    mock_func.reset_mock()
    ext.call('input_files', 'output_files', 'workspace', {'x': '5', 'y': 2.71})
    assert mock_func.called

    called_args, _ = mock_func.call_args
    assert called_args[0] == 'input_files'
    assert called_args[1] == 'output_files'
    assert called_args[2] == 'workspace'
    assert called_args[3]['x'] == 5
    assert called_args[3]['y'] == 2.71
