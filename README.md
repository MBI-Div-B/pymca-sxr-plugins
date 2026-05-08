# pymca-sxr-plugins

Plugins to handle special cases of online data evaluation using PyMca.

## How to access plugins in PyMca
- select curve of spec file
- select cog icon above plot window
- 'Set User Plugin Directory'
- 'Reload Plugins'
- click on the Plugin Name 'Skip Points Plugin'
- and select an operation to perform on the selected curve

- alternatively the plugins can be put into '/home/labuser/.pymca/plugins'
- and PyMca will automatically detect them as this is the default user plugin directory

- if PyMca does not show the plugin, it was not loaded as there might have been an error in the code
- debug by running PyMca in the terminal: 'pymca --debug=1'

## SkipPointsPlugin

- used to handle data points created using a toggle scan
- used for XMCD measurements -> alternating the B field during a scan
- sperates the data points and calculates the average assuming a dummy scan structure