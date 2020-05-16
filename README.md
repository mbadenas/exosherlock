<p align="center">
	<img src="https://github.com/mbadenas/exosherlock/blob/master/doc/logo/exosherlock_logo.png" height=250></img>
</p>

# exosherlock

 `exosherlock` is an open-source package designed to interact with and download the [planetary systems catalogs](https://exoplanetarchive.ipac.caltech.edu/docs/data.html) of the NASA Exoplanet Archive in a consistent and reliable way. Through its user-friendly interface, `exosherlock` provides the user with the possibility to: 
 
- Download the most up-to-date catalog of [Confirmed Planets](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets)<sup>1,2</sup>, or
- Query and retrieve a Planetary Systems catalog of their choice (see options [here](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.htmll)), or
- Load a local Planetary Systems catalog, previously downloaded by the user from the NASA Exoplanet Archive. Such catalog may, e.g., only contain a subset of all the columns listed on the full Planetary Systems catalog. 

<font size="0.5"> (1) Last Update of `exosherlock`'s internal catalog: May 2020</font>
<font size="0.5"> (2) A future release of `exosherlock` will use the new *alpha release* Planetary Systems catalog from the Archive.</font>

## Documentation

The software's documentation can be found [here](https://mbadenas.github.io/exosherlock/index.html).
First time users may find the [quickstart](https://mbadenas.github.io/exosherlock/quickstart.html) helpful. 

## Installation

### Stable
The most recent version of `exosherlock is available on [PyPI](https://pypi.org/project/exosherlock/).
The latest stable version can be installed using pip:

```
pip install sherlock
```

### Development
The latest development version can be installed from the master branch using pip:

```
pip install git+git://github.com/mbadenas/exosherlock.git
```

## Attribution
If you use this code, please cite `exosherlock` in your work. The citatation in BibTeX format is presented below. 

```
@misc{exosherlock,
  auhor = {{Badenas-Agusti}, M. and {Abril-Pla}, O.},
  title = {exosherlock: Data Acquisition from the NASA Exoplanet Archive.},
  year  = {2020},
  url   = {https://github.com/mbadenas/exosherlock},
}
```

## Authorship and Contributions

**Authors**: Mariona Badenas-Agusti (MIT), Oriol Abril-Pla (UpF)

**License**: MIT. 

**Contributors**: `exosherlock` welcomes feedback and contributions. Before submitting a Pull Request for a
new feature, please open an issue to discuss its inclusion and implementation details.

## Code of Conduct
`exosherlock` wishes to maintain a positive community. Additional details
can be found in the [Code of Conduct](https://github.com/mbadenas/exosherlock/blob/master/CODE_OF_CONDUCT.md).
