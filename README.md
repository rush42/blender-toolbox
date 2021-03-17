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
Extends the file menu with a button for incremental saving.
After invoking Incremental saving the trailing number of the project file name gets increased.
If there is no number at the end of the project file name "_001" gets concatenated.
