#!/usr/bin/env python3


"""
Instructions

- Functions intended to run for each scan
  need to be named run_xxxxx

- Do not modify the parameters of the run_xxx function
  unless you know what you are doing
  see optional parameters:
  https://github.com/tangible-landscape/grass-tangible-landscape/wiki/Running-analyses-and-developing-workflows#python-workflows

- All gs.run_command/read_command/write_command/parse_command
  need to be passed env parameter (..., env=env)
"""

import grass.script as gs


def run_summitFinder(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.geomorphon",
        elevation=scanned_elev,
        forms="geomorph",
        search=30,
        skip=0,
        flat=1,
        dist=0,
        env=env,
    )
    gs.mapcalc("'summits' = if(geomorph == 2, 1, null())", env=env)
    gs.run_command("r.thin", input="summits", output="summits_thinned", env=env)
    gs.run_command(
        "r.to.vect", input="summits_thinned", output="summits", type="point", env=env
    )


def run_contours(scanned_elev, env, **kwargs):
    interval = 5
    gs.run_command(
        "r.contour",
        input=scanned_elev,
        output="contours",
        step=interval,
        flags="t",
        env=env,
    )


# this part is for testing without TL
def main():
    import os

    # get the current environment variables as a copy
    env = os.environ.copy()
    # we want to run this repetetively without deleted the created files
    env["GRASS_OVERWRITE"] = "1"

    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    # resampling to have similar resolution as with TL
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    # this will run all 3 examples (slope, contours, points)
    run_summitFinder(scanned_elev=elev_resampled, env=env)
    run_contours(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
