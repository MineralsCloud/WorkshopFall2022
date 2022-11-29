import click

@click.command()
@click.option("--iv", type=click.INT)
@click.option("--iq", type=click.INT)
@click.option("--ip", type=click.INT)
@click.option("--pivot", is_flag=True)
@click.argument("input01")
def main(input01, **kwargs):

    import sys, pandas, numpy

    df = []

    with open(input01) as fp:
        for _ in range(3): next(fp)
        nv, nq, np, nm, na = [int(x) for x in next(fp).strip().split()]
        next(fp)

        for i in range(nv):
            line = next(fp)

            P, V, E = [float(x) for x in line.strip().split()[1::2]]
            # df.loc[idx, "pressure"] = P
            # df.loc[idx, "volume_"] = V
            # df.loc[idx, "energy"] = E

            for j in range(nq):
                line = next(fp)
                # kp.write(line)
                for k in range(np):
                    line = next(fp)
                    freq = float(line)

                    df.append({
                        "P": P,
                        "V": V,
                        "E": E,
                        "iv": i,
                        "iq": j,
                        "ip": k,
                        "freq": freq,
                    })

            # next(fp)

    df = pandas.DataFrame(df)

    iv = kwargs.pop("iv", None)
    if iv != None: df = df[df["iv"] == iv]

    iq = kwargs.pop("iq", None)
    if iq != None: df = df[df["iq"] == iq]

    ip = kwargs.pop("ip", None)
    if ip != None: df = df[df["ip"] == ip]

    if kwargs.pop("pivot", False) and ((iq != None) or (ip != None)):
        df = df.pivot(columns="V", index="ip" if iq != None else "iq", values="freq")
        del df.index.name
        df = df.drop(1120.2235, axis=1)
        sys.stdout.write(df.to_string())
    else:
        sys.stdout.write(df.to_string(index=None))
    

if __name__ == "__main__":
    main()