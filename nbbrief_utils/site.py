from ipywidgets import Checkbox, jslink, jsdlink, RadioButtons
from functools import partial
from pathlib import Path
from papermill.iorw import load_notebook_node
from papermill.parameterize import parameterize_notebook
from nbconvert import HTMLExporter
from traitlets.config import Config

myCheckbox = partial(Checkbox,
        disabled=False,
        layout={'width': 'initial'}
        )

def make_page_navs(pages, nav_prefix=''):
    """Generate the markdown page navigation
    links for a list of active pages."""

    enabled_pages = [pg for pg in pages if pg.enabled]

    nav_template = nav_prefix + ' | {} | {}'

    pgs_nav_md = []

    len_pages = len(enabled_pages)

    for i in range(len_pages):
        try:
            # avoid special case where we start counting back from end
            assert i > 0
            prv_Page = enabled_pages[i - 1]
            prv_md = f"[previous]({prv_Page.name + '.html'})"
        except:
            prv_md = '~~previous~~'

        try:
            nxt_Page = enabled_pages[i + 1]
            nxt_md = f"[next]({nxt_Page.name + '.html'})"
        except:
            nxt_md = '~~next~~'

        pgs_nav_md.append(nav_template.format(prv_md, nxt_md))

    return list(zip(enabled_pages, pgs_nav_md))

def make_log_level_radio(logger, value='WARNING'):
    """Create a radio button to easily
    set the log level, interactively."""
    log_lvl_rad_btn = RadioButtons(
            description = 'log level',
            options = [
                'DEBUG',
                'INFO',
                'WARNING',
                'ERROR',
                'CRITICAL',
                ],
            value = value.upper()
            )

    def rad_changed(change):
        logger.setLevel(change['new'])

    log_lvl_rad_btn.observe(rad_changed, names = 'value')

    return log_lvl_rad_btn

def insert_params_cell(nb_path, parameters=dict()):
    """Wrap papermill to inject the cell
    used to override specified variables
    in the 'parameters' tagged cell.
    returns: nbformat notebook Node"""
    # `load_notebook_node` works around parametrize . . .
    # choking on cells without 'tags'
    return parameterize_notebook(
            load_notebook_node(str(nb_path)),
            parameters=parameters,
            comment='injected-paramters'
            )

def write_html_grid(nb_node, out_path='test.html', config=None):
    """Wrap nb_convert to render notebook node
    to nbconvert Dejavu(Voila)-like output."""

    # Set configuration to mimick what Dejavu does to mimick
    # Voila, plus use gridstack template for layout
    c = Config()
    c.TemplateExporter.exclude_input = True
    c.TemplateExporter.exclude_output_prompt = True
    c.TemplateExporter.exclude_input_prompt = True
    c.ExecutePreprocessor.enabled=True
    c.HTMLExporter.template_name = 'gridstack'

    # just in case the user wants to add some
    # more customizations
    if config is not None:
        c.merge(config)

    out_path = Path(out_path)

    # Generate the HTML text
    (body, resources) = HTMLExporter(config=c).from_notebook_node(nb_node)

    # return a report message while writing to the out_path file
    return f"{out_path.write_text(body)} bytes written to {out_path}"

def generate_page(nb_path, web_root="../www", params={}):
    """Generate a gridstack html page from a notebook"""
    nb_path = Path(nb_path)

    html_out_path = Path(web_root) / (nb_path.stem + '.html')

    nb_node = insert_params_cell(nb_path, parameters=params)

    return write_html_grid(nb_node, out_path=html_out_path)
