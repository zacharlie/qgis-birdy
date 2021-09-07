# Birdy

Fly to location and zoom

## About

Minimalist QGIS plugin for allowing user to center the QGIS canvas on a geographic position at a user defined scale

### Configuration

You can configure the project variables `birdy_x`, `birdy_y`, `birdy_scale` for configuring the default values

### Installation

Just unzip to the relevant user profiles `python\plugins` directory

### Disclaimer

Experimental pre-alpha: it will eat your homework

### Usage

Input geographic coordinates and scale in XYZ and click the birdy to fly. 0 resets the default values.

![birdy](https://user-images.githubusercontent.com/64078329/132323368-42937760-7399-4236-b538-8ef4a39dc4c7.gif)

### Alternatives

QGIS natively provides the Coordinate window for navigating to a position in map coordinates. The `go` function available in the locator bar allows users to choose between centering on map coordinates and geographic coordinates. The QGIS interface provides the option of setting map Scale. Birdy just does the map centering and scaling together, but currently it only provides support for geographic coordinates.
