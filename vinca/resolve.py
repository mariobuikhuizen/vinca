def get_conda_index(vinca_conf):
    import ruamel.yaml

    yaml = ruamel.yaml.YAML()
    conda_index = []
    for i in vinca_conf['conda_index']:
        conda_index.append(yaml.load(open(i, 'r')))
    return conda_index


def resolve_pkgname_from_indexes(pkg_shortname, conda_index):
    for i in conda_index:
        if pkg_shortname in i:
            # TODO: replace with platform variable.
            platform = 'unix'
            if platform in i[pkg_shortname].keys():
                return i[pkg_shortname][platform]
            elif 'any' in i[pkg_shortname].keys():
                return i[pkg_shortname]['any']
            raise KeyError("Missing package for platform {}: {}\nCheck your conda metadata!".format(platform, pkg_shortname))
    return None


def resolve_pkgname(pkg_shortname, vinca_conf, distro):
    pkg_names = resolve_pkgname_from_indexes(
        pkg_shortname, vinca_conf['_conda_indexes'])
    if pkg_names is None:
        if not distro.check_package(pkg_shortname):
            return []
        else:
            return ['ros-%s-%s' %
                    (vinca_conf['ros_distro'],
                     pkg_shortname.replace('_', '-'))]
    else:
        return pkg_names
