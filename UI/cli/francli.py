import click
import soc as SoCActions

@click.group()
def cli():
    pass

#### Start SoC Group
@cli.group()
def soc():
    pass

# @soc.command()
# def init():
#     SoCActions.init()
#     # click.echo("Initializing SoC...")

@soc.command()
def status():
    #TODO
    SoCActions.cat_config()
    click.echo("SoC status...")

@soc.group()
def set():
    pass

@set.command()
def channel_freq():
    #TODO
    click.echo("Set channel frequency...")

@set.command()
def data_source():
    #TODO
    click.echo("Set data source...")

@set.command()
def band_filter():
    #TODO
    click.echo("Set band filter...")

@set.command()
def channel_filter():
    #TODO
    click.echo("Set channel filter...")
#### End SoC Group


#### Start SDR Group
@cli.group()
def sdr():
    pass

@sdr.command()
def status():
    #Todo
    click.echo("SDR status...")

@sdr.command()
def calibrate():
    #Todo
    click.echo("Calibrate...")

@sdr.command()
def waterfall():
    #Todo
    click.echo("Waterfall...")
#### End SDR Group


#### Start Server Group
@cli.group()
def server():
    pass

@server.command()
def init():
    #TODO
    click.echo("Initializing server")

@server.command()
def status():
    #TODO
    click.echo("Server status...")
#### End Server Group