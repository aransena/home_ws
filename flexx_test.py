from flexx import app, ui

m = app.launch(ui.Widget)  # Main widget

b1 = ui.Button(text='Hello', parent=m)
b2 = ui.Button(text='world', parent=m)

app.run()