class Module:
    """
    Basic module class. All modules should inherit from this class.
    """

    def __init__(self, name):
        """
        Use this constructor to set the name of the module. It should store all the needed information for ``runModule`` method.

        Parameters
        ----------
        name : str
            Name of the module
        """
        self.name = name

    def runModule(self, df, values):
        """
        The main method of the module. It should contain all the logic of the module.

        Parameters
        ----------
        df : mRDF
            The ``mRDF`` dataframe
        values : list
            List of values that are passed between modules (should contain efficiency of cuts and other values)

        Returns
        -------
        mRDF
            The modified mRDF dataframe
        """
        return df

    def run(self, df, values):
        """
        No module should overwrite this method. It is used to store the efficiency of the module.

        Parameters
        ----------
        df : mRDF
            The ``mRDF`` dataframe
        values : list
            List of values that are passed between modules (should contain efficiency of cuts and other values)

        Returns
        -------
        mRDF
            The modified mRDF dataframe
        """
        values.append([df.Count(), "begin count of " + self.name])
        a = len(values) - 1

        df = self.runModule(df, values)

        values.append([df.Count(), "end count of " + self.name])
        b = len(values) - 1

        def fun(a, b):
            bVal = values[b]
            aVal = values[a]
            if "list" in str(type(bVal)):
                bVal = bVal[0]
            if "list" in str(type(aVal)):
                aVal = aVal[0]
            if 0 != aVal.GetValue():
                return [
                    f"Efficiency of {self.name} module",
                    str(round(bVal.GetValue() / aVal.GetValue() * 100, 3)) + "%",
                ]
            else:
                return [
                    f"Efficiency of {self.name} module",
                    "0.000%",
                ]

        values.append([fun, a, b])
        return df
