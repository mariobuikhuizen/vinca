import datetime
import ruamel
import os

TEMPLATE = """\
package:
  name: ros
  version: 0.0.1

source:

build:
  number: 0

about:
  home: https://www.ros.org/
  license: BSD-3-Clause
  summary: |
    Robot Operating System

extra:
  recipe-maintainers:
    - ros-forge
"""


def write_recipe(source, outputs, single_file=True):
    # single_file = False
    if single_file:
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        meta = yaml.load(TEMPLATE)

        meta['source'] = [source[k] for k in source]
        meta['outputs'] = outputs
        meta['package']['version'] = f"{datetime.datetime.now():%Y.%m.%d}"

        with open("meta.yaml", 'w') as stream:
            yaml.dump(meta, stream)
    else:
        for o in outputs:
            yaml = ruamel.yaml.YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)
            meta = yaml.load(TEMPLATE)

            meta['source'] = source[o['name']]
            for k, v in o.items():
                meta[k] = v

            meta['package']['name'] = o['name']
            meta['package']['version'] = o['version']

            if not os.path.isdir("recipes"):
                os.makedirs("recipes")
            with open(os.path.join("recipes", f"{o['name']}.yaml"), 'w') as stream:
                yaml.dump(meta, stream)

def generate_template(template_in, template_out):
    import em
    g = {
      'ros_distro': os.environ['ROS_DISTRO']
    }
    interpreter = em.Interpreter(
      output=template_out,
      options={em.RAW_OPT: True, em.BUFFERED_OPT: True})
    interpreter.updateGlobals(g)
    interpreter.file(open(template_in))
    interpreter.shutdown()


def generate_bld_ament_cmake():
    import pkg_resources
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/bld_ament_cmake.bat.in')
    generate_template(template_in, open('bld_ament_cmake.bat', 'w'))


def generate_bld_ament_python():
    import pkg_resources
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/bld_ament_python.bat.in')
    generate_template(template_in, open('bld_ament_python.bat', 'w'))


def generate_bld_catkin():
    import pkg_resources
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/bld_catkin.bat.in')
    generate_template(template_in, open('bld_catkin.bat', 'w'))
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/build_catkin.sh.in')
    generate_template(template_in, open('build_catkin.sh', 'w'))


def generate_bld_colcon_merge():
    import pkg_resources
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/bld_colcon_merge.bat.in')
    generate_template(template_in, open('bld_colcon_merge.bat', 'w'))


def generate_bld_catkin_merge():
    import pkg_resources
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/bld_catkin_merge.bat.in')
    generate_template(template_in, open('bld_catkin_merge.bat', 'w'))


def generate_activate_hook():
    import pkg_resources
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/activate.bat.in')
    generate_template(template_in, open('activate.bat', 'w'))
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/deactivate.bat.in')
    generate_template(template_in, open('deactivate.bat', 'w'))
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/activate.sh.in')
    generate_template(template_in, open('activate.sh', 'w'))
    template_in = pkg_resources.resource_filename(
      'vinca', 'templates/deactivate.sh.in')
    generate_template(template_in, open('deactivate.sh', 'w'))
