def flatten_samples(samples):
    """
    flatten the subsamples (create full samples named sample_subsample, or flatten_samples_map(sample, subsample))

    Parameters
    ----------
    samples : dict
        samples dictionary, will be modified in place

    Returns
    -------
    list
        subsamplesmap is returned e.g. ``[(sample, [sample_subsample1, sample_subsample2])]``
    """
    subsamplesmap = []
    for sname in list(samples.keys()):
        sample = samples[sname]
        if "subsamples" not in sample:
            continue
        active_fsm = samples[sname].get(
            "flatten_samples_map", 0
        )
        if active_fsm == 0:  flatten_samples_map = lambda sname, sub: "%s_%s" % (sname, sub)
        else: flatten_samples_map = lambda sname, sub: "%s" % (sub)
        
        subsamplesmap.append((sname, []))
        for sub in sample["subsamples"]:
            new_subsample_name = flatten_samples_map(sname, sub)
            samples[new_subsample_name] = sample
            subsamplesmap[-1][1].append(new_subsample_name)

        sample.pop("subsamples")
        samples.pop(sname)

    return subsamplesmap


def flatten_cuts(cuts):
    """
    flatten the categories (create full cuts named cut_category)

    Parameters
    ----------
    cuts : dict
        cuts dictionary, will be modified in place

    Returns
    -------
    list
        categoriesmap is returned e.g. ``[(cut, [cut_category1, cut_category2])]``
    """
    categoriesmap = []
    for cname in list(cuts.keys()):
        cut = cuts[cname]
        if "categories" not in cut:
            continue

        categoriesmap.append((cname, []))
        for cat in cut["categories"]:
            cuts["%s_%s" % (cname, cat)] = cut
            categoriesmap[-1][1].append("%s_%s" % (cname, cat))

        cut.pop("categories")
        cuts.pop(cname)

    return categoriesmap


def update_variables_with_categories(variables, categoriesmap):
    """
    Update variables dict with the flatten categories.
    variables can have "cuts" specifications

    Parameters
    ----------
    variables : dict
        variables dictionary, will be modified in place
    categoriesmap : list
        categoriesmap as returned by flatten_cuts
    """
    for variable in variables.items():
        if "cuts" not in variable:
            continue

        cutspec = variable["cuts"]

        for cname, categories in categoriesmap:
            if cname not in cutspec:
                continue

            # original cut is in the spec
            cutspec.remove(cname)

            # if a category (subcut) is also in the spec, we won't touch this variable
            if len(set(cutspec) & set(categories)) != 0:
                continue

            # otherwise we replace the cut with all the categories
            cutspec.extend(categories)


def update_nuisances_with_subsamples(nuisances, subsamplesmap):
    """
    Update nuisances dict with the flatten subsamples.

    Parameters
    ----------
    nuisances : dict
        nuisances dictionary, will be modified in place
    subsamplesmap : list
        subsamplesmap as returned by flatten_samples
    """
    for nuisance in nuisances.items():
        if "samples" not in nuisance:
            continue

        samplespec = nuisance["samples"]

        for sname, subsamples in subsamplesmap:
            if sname not in samplespec:
                continue

            # original sample is in the spec
            sconfig = samplespec.pop(sname)

            # if a subsample is also in the spec, we won't toucn this any more
            if len(set(samplespec.keys()) & set(subsamples)) != 0:
                continue

            # otherwise we replace the sample with all the subsamples
            samplespec.update((subsample, sconfig) for subsample in subsamples)


def update_nuisances_with_categories(nuisances, categoriesmap):
    """
    Update nuisances dict with the flatten categories.

    Parameters
    ----------
    nuisances : dict
        nuisances dictionary, will be modified in place
    categoriesmap : list
        categoriesmap as returned by flatten_samples
    """
    for nuisance in nuisances.values():
        if "cuts" not in nuisance:
            continue

        cutspec = nuisance["cuts"]

        for cname, categories in categoriesmap:
            if cname not in cutspec:
                continue

            # original cut is in the spec
            cutspec.remove(cname)

            # if a category (subcut) is also in the spec, we won't touch this nuisance
            if len(set(cutspec) & set(categories)) != 0:
                continue

            # otherwise we replace the cut with all the categories
            cutspec.extend(categories)
