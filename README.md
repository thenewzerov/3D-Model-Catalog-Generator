# 3D Model Cataloger

This project is used to create an HTML file that lists all the 3D models in a directory.
It's mostly setup for how I need, but if you want to follow my naming and organization conventions, you can use it too.
The HTML file is created in the same directory as the script and is named `output.html`.

Tags you've added to your models will be included at the top as filters, and there will be a search bar.
Honestly, try and keep filters to a minimum, unless you want to tweak the CSS for me.

## Usage

To use this script, run it and pass the path to the directory containing the 3D models as an argument.

Run a pip install to install the required packages.
```bash
pip install -r requirements.txt
```
Then run the script

```bash
python3 main.py "/path/to/3D Models"
```

If your directories have a `model-info.txt` file in them, use the following flag to run them.

```bash
python3 main.py "/path/to/3D Models" --use-model-info
``` 

## Directory Structure

The script expects the directory to have the following structure.
If the directory has is surrounded with `{}` then it can be any name.

There can be any number of directories between Category and Series Name.

The `model-info.txt` file is optional, but if you're going to use it, 
it should be in the same directory as the base image file.

```
3D Models
- {Category 1}
    ...
  - {Series Name}
    - {Model Name}
        - STL
        - Renders
        - Zips
        - {image file}
        - model-info.txt
- {Category 2}
    ...
    - {Series Name}
        - {Model Name}
            - STL
            - Renders
            - Zips
            - {image file}
            - model-info.txt
```

## Naming Conventions

The only important naming convention is the Model Name Directory.
While only the Model Name is required, if you're going to add the rest, follow this format (including spaces):

```
{Model Name}_{Model Variant} {Number} - {Space Separated Tags}
```

### Sample Valid Model Names

* Millennium Falcon
* Millennium Falcon_Original Trilogy
* Millennium Falcon 2
* Millennium Falcon - Prequel FDM
* Millennium Falcon_Original Trilogy 5
* Millennium Falcon_Sequel Trilogy 2 - Sequel FDM



### Example

Say you have 3 different 3d models of the Millennium Falcon.  
* One is the original trilogy version and the other is the sequel trilogy version.
* You want to tag one as being a pre-supported model, and both as made for FDM printing.
* You want to add a number to one of the names (because you've reorganized your models a million times trying to get it right).
* The root directory is named '3D Models'

Your directory structure would be as follows:

```
3D Models
 - Movies
    - Star Wars
      - Millennium Falcon
        - Millennium Falcon_Original Trilogy - Prequel FDM
          - STL
          - Renders
          - Zips
          - {image file}
        - Millennium Falcon_Sequel Trilogy - Sequel FDM
          - STL
          - Renders
          - Zips
          - {image file}
        - Millennium Falcon_Sequel Trilogy 2 - Sequel FDM
          - STL
          - Renders
          - Zips
          - {image file}
```

This would generate an html table that looks like this:

| Character Name    | Model Name                           | Series    | Model Category | Tags         | Image             |
|-------------------|--------------------------------------|-----------|----------------|--------------|-------------------|
| Millennium Falcon | Millennium Falcon - Original Trilogy | Star Wars | Movies         | Prequel, FDM | An embedded image |
| Millennium Falcon | Millennium Falcon - Sequel Trilogy   | Star Wars | Movies         | Sequel, FDM  | An embedded image |
| Millennium Falcon | Millennium Falcon - Sequel Trilogy 2 | Star Wars | Movies         | Sequel, FDM  | An embedded image |


## Special Tags

The only "special" tag is `NSFW`.  If you add this tag to a model, the image will be blurred.

## Helper Scripts

### Missing Directories

There's a helper script in here too called `invalid.py`. 
It's used to find folders that don't match the directory structure.

Run it the same way as the main script, but it will print out the folders that don't match the structure.

```bash
python3 invalid.py "/path/to/3D Models"
```

### Directory Renamer

There's another helper script called `directory_rename.py`.

Don't use this one.  It's made for how I had my folders named before.
It's not going to be useful for you unless you have the same naming conventions.
The structure is there for finding the directories and everything, but you'd have to change it to work.
In case you decide to run it anyways, I've commented out the actual "renaming" part of the script.
You've been warned.

### Generate Model Info

There's a helper script called `generate_model_info.py`.

This script will generate a `model-info.txt` file in each model directory.
A sample file would look like this:

```
Model Name: Millennium Falcon
Character Name: Millennium Falcon
Series: Star Wars
Model Category: Movies
Tags: Prequel, FDM
```

This only works if you have the correct directory structure and naming conventions.
Mostly useful if you're going to switch to using the model-info.txt files instead of the naming conventions.
Although I recommend using both, because the naming conventions are useful for sorting and filtering.

## Final Notes

This script is very specific to my needs, you're free to use it, or if you have suggestions let me know.
If you really do have a good suggestion, try to include something that would help me rename all my existing folders!

Also, not sure if the numbers are going to stick around or not, try not to use them in your naming just in case.
