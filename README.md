# blender-toolbox
This collection is intended to make the use of blender more comfortable and easy.

## Token Substituter
Replaces the following tokens in paths used for compositing nodes and render output.

| Token       | Value             |
|-------------|-------------------|
| $prj        | Project name      |
| $camera     | Active Camera     |
| $res        | Render resolution |
| $CVCOMPUTER | Hostname          |
| $CVUSERNAME | Username          |
| $CVRENDERER | Render engine     |
| $YYYY/$YY   | Year              |
| $MM         | Month             |
| $DD         | Day               |
| $H          | Hour              |
| $M          | Minute            |
| $s          | Second            |


## Save Incremental
Adds an operator for incremental saving, where the project name gets increased every invocation.
Extends the file menu with a button for incremental saving.
