## Polars

### Data Types
Polars, similarly to pandas, also provides us **Series** and **Dataframes**. 
1. Series are one dimensional in nature, think a single column with a name. 
2. Dataframes are 2d in nature, think a table, with each table having a name.

### Key conceptual and usage differences with pandas
1. DataTypes
    - **Same data types in a series**, below example is invalid
        <br>

            s1 = pl.Series([1, 2, 3, 4, 'srajan'])
        This throws an error to us, because the last value isn't an integer. Unlike pandas, where this syntax is perfectly valid.
        ```python
            s1 = pd.Series([1, 2, 3, 4, 'srajan'])
        ```
        BTW, we can set strict to False to allow values of different data types.
        ```python
            pl.Series([1, 2, 3, 4, 'srajan'], strict=False)
        ```
    - Similarly, each individual series in a dataframe must be of the same type.

2. Optimization
    - It uses Arrow arrays under the hood, which are more efficient than pandas' numpy arrays (pandas also allows for arrow data structure in newer versions).
    - It uses a lazy evaluation model, only compute when needed.

<br>
Throughout the notes we'll majorly be dealing with the below dataframe
<br>

    df = pl.DataFrame(
        {
            "name": ["Alice Archer", "Ben Brown", "Chloe Cooper", "Daniel Donovan"],
            "birthdate": [
                date(1997, 1, 10),
                date(1985, 2, 15),
                date(1983, 3, 22),
                date(1981, 4, 30),
            ],
            "weight": [57.9, 72.5, 53.6, 83.1],  # (kg)
            "height": [1.56, 1.77, 1.65, 1.75],  # (m)
        }
    )

        ┌────────────────┬────────────┬────────┬────────┐
        │ name           ┆ birthdate  ┆ weight ┆ height │
        │ ---            ┆ ---        ┆ ---    ┆ ---    │
        │ str            ┆ date       ┆ f64    ┆ f64    │
        ╞════════════════╪════════════╪════════╪════════╡
        │ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   │
        │ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   │
        │ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   │
        │ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   │
        └────────────────┴────────────┴────────┴────────┘
<br>

### Polars important syntax 
1. Expressions
    <br>
    Expressions in polars are a powerful feature. Consider below expression
    ```python
    pl.col("weight") / (pl.col("height") ** 2)
    ```
    If you print this, then you will get this
    ```bash
    [(col("weight")) / (col("height").pow([dyn int: 2]))]
    ```
    Notice that any computation has not been done. Polars does not do any computation for just the expression, only when we put in some context (`select, with_columns, filter, group_by`) then it yields results.
2. Inspecting dataframes
    - `head()`
    <br>
    Returns the head of dataframe in syntax of a table
    - `describe()`
    <br>
    Describes the statistics of the dataframe.
    - `shape`
    <br>
    Returns the shape of the dataframe in a tuple format. First element is the number of rows and second element is the number of columns.
    - `schema`
    <br>
    Returns the data types of the dataframe in a dictionary format. The keys are the column names and the values are the data types.
    - `columns`
    <br>
    Returns the columns of the dataframe in a list format. The elements are the column names.

3. Basic operations
    * Basic arithematic
    <br>
        ```python
            result = df.select((pl.col('height') * 100).alias('height in cm'))
        #output
        It outputs a df which has one col, "height in cm".
        ```
    * Comparison ops
        ```python
            result = df.select((pl.col('height') > 1.6).alias('tall people'))
        #output
        It outputs a df which has one col, "height in cm".
        ```

4. Laziness and contexts
    - Laziness
    <br>Polars is lazy by default, consider below example.
        ```python
        bmi_expr = pl.col('weight')/(pl.col('height')**2)
        print(bmi_expr)
        # output    [(col("weight")) / (col("height").pow([dyn int: 2]))]
        ```
        Because expressions are lazy, no computations have taken place yet. Hence, if you want them to produce a result, you must be using them inside a context.
    - Contexts
    <br>Polars provides following contexts, inside of which we can use these expressions.
    <br>
        1. select
            <br>Does not include the columns of df, only the ones specified in `select`
            ```python
            result = df.select(
                bmi=bmi_expr,
                ideal_max_bmi=25,
            )
            print(df)
            #output is below
            shape: (4, 2)
            ┌───────────┬───────────────┐
            │ bmi       ┆ ideal_max_bmi │
            │ ---       ┆ ---           │
            │ f64       ┆ i32           │
            ╞═══════════╪═══════════════╡
            │ 23.791913 ┆ 25            │
            │ 23.141498 ┆ 25            │
            │ 19.687787 ┆ 25            │
            │ 27.134694 ┆ 25            │
            └───────────┴───────────────┘
            ```
            The bmi above is a series, and the ideal_max_bmi is a scalar value which gets broadcasted. If there are multiple series, all must be off same length.
        2. with_columns
            <br>Pretty much same as select, only difference is that the output df will have all the column of original df, hence the newly added Series must be of same length as existing series inside the df
            ```python
            result = df.with_columns(
                bmi=bmi_expr,
                ideal_max_bmi=25,
            )

            #output 
            shape: (4, 6)
            ┌────────────────┬────────────┬────────┬────────┬───────────┬───────────────┐
            │ name           ┆ birthdate  ┆ weight ┆ height ┆ bmi       ┆ ideal_max_bmi │
            │ ---            ┆ ---        ┆ ---    ┆ ---    ┆ ---       ┆ ---           │
            │ str            ┆ date       ┆ f64    ┆ f64    ┆ f64       ┆ i32           │
            ╞════════════════╪════════════╪════════╪════════╪═══════════╪═══════════════╡
            │ Alice Archer   ┆ 1997-01-10 ┆ 57.9   ┆ 1.56   ┆ 23.791913 ┆ 25            │
            │ Ben Brown      ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   ┆ 23.141498 ┆ 25            │
            │ Chloe Cooper   ┆ 1983-03-22 ┆ 53.6   ┆ 1.65   ┆ 19.687787 ┆ 25            │
            │ Daniel Donovan ┆ 1981-04-30 ┆ 83.1   ┆ 1.75   ┆ 27.134694 ┆ 25            │
            └────────────────┴────────────┴────────┴────────┴───────────┴───────────────┘   
            ```
        3. filter
            <br>Apply conditions on df's columns, returns a new df with the conditions applied.
            ```python
            result = df.filter(
                pl.col("birthdate").is_between(date(1982, 12, 31), date(1996, 1, 1)),
                pl.col("height") > 1.7,
            )
            #output
            shape: (1, 4)
            ┌───────────┬────────────┬────────┬────────┐
            │ name      ┆ birthdate  ┆ weight ┆ height │
            │ ---       ┆ ---        ┆ ---    ┆ ---    │
            │ str       ┆ date       ┆ f64    ┆ f64    │
            ╞═══════════╪════════════╪════════╪════════╡
            │ Ben Brown ┆ 1985-02-15 ┆ 72.5   ┆ 1.77   │
            └───────────┴────────────┴────────┴────────┘    
            ```
        4. group_by 
            <br> Consider below example
            ```python
            result = df.group_by(
                (pl.col("birthdate").dt.year() // 10 * 10).alias("decade"),
            ).agg(pl.col('name'))
            ```
            This will divide the year by 100 for each row, and rows which end up having the same values will be grouped. Hence the output is 
            shape: (2, 2)
            ```python
            ┌────────┬─────────────────────────────────┐
            │ decade ┆ name                            │
            │ ---    ┆ ---                             │
            │ i32    ┆ list[str]                       │
            ╞════════╪═════════════════════════════════╡
            │ 1990   ┆ ["Alice Archer"]                │
            │ 1980   ┆ ["Ben Brown", "Chloe Cooper", … │
            └────────┴─────────────────────────────────┘
            ``` 
---
<br>

Let's switch to a different df for the next section
```python
import polars as pl

df = pl.DataFrame(
    {  # As of 14th October 2024, ~3pm UTC
        "ticker": ["AAPL", "NVDA", "MSFT", "GOOG", "AMZN"],
        "company_name": ["Apple", "NVIDIA", "Microsoft", "Alphabet (Google)", "Amazon"],
        "price": [229.9, 138.93, 420.56, 166.41, 188.4],
        "day_high": [231.31, 139.6, 424.04, 167.62, 189.83],
        "day_low": [228.6, 136.3, 417.52, 164.78, 188.44],
        "year_high": [237.23, 140.76, 468.35, 193.31, 201.2],
        "year_low": [164.08, 39.23, 324.39, 121.46, 118.35],
    }
)

# output
shape: (5, 7)
┌────────┬───────────────────┬────────┬──────────┬─────────┬───────────┬──────────┐
│ ticker ┆ company_name      ┆ price  ┆ day_high ┆ day_low ┆ year_high ┆ year_low │
│ ---    ┆ ---               ┆ ---    ┆ ---      ┆ ---     ┆ ---       ┆ ---      │
│ str    ┆ str               ┆ f64    ┆ f64      ┆ f64     ┆ f64       ┆ f64      │
╞════════╪═══════════════════╪════════╪══════════╪═════════╪═══════════╪══════════╡
│ AAPL   ┆ Apple             ┆ 229.9  ┆ 231.31   ┆ 228.6   ┆ 237.23    ┆ 164.08   │
│ NVDA   ┆ NVIDIA            ┆ 138.93 ┆ 139.6    ┆ 136.3   ┆ 140.76    ┆ 39.23    │
│ MSFT   ┆ Microsoft         ┆ 420.56 ┆ 424.04   ┆ 417.52  ┆ 468.35    ┆ 324.39   │
│ GOOG   ┆ Alphabet (Google) ┆ 166.41 ┆ 167.62   ┆ 164.78  ┆ 193.31    ┆ 121.46   │
│ AMZN   ┆ Amazon            ┆ 188.4  ┆ 189.83   ┆ 188.44  ┆ 201.2     ┆ 118.35   │
└────────┴───────────────────┴────────┴──────────┴─────────┴───────────┴──────────┘
```

4. Expression expansion
    - Expansion using column name
        ```python
        eur_usd_rate = 1.09  # As of 14th October 2024

        result = df.with_columns(
            (
                pl.col(
                    "price",
                    "day_high",
                    "day_low",
                    "year_high",
                    "year_low",
                )
                / eur_usd_rate
            ).round(2)
        )
        #output
        ┌────────┬───────────────────┬────────────┬────────────┬────────────┬────────────┬────────────┐
        │ ticker ┆ company_name      ┆ price      ┆ day_high   ┆ day_low    ┆ year_high  ┆ year_low   │
        │ ---    ┆ ---               ┆ ---        ┆ ---        ┆ ---        ┆ ---        ┆ ---        │
        │ str    ┆ str               ┆ f64        ┆ f64        ┆ f64        ┆ f64        ┆ f64        │
        ╞════════╪═══════════════════╪════════════╪════════════╪════════════╪════════════╪════════════╡
        │ AAPL   ┆ Apple             ┆ 210.917431 ┆ 212.211009 ┆ 209.724771 ┆ 217.642202 ┆ 150.53211  │
        │ NVDA   ┆ NVIDIA            ┆ 127.458716 ┆ 128.073394 ┆ 125.045872 ┆ 129.137615 ┆ 35.990826  │
        │ MSFT   ┆ Microsoft         ┆ 385.834862 ┆ 389.027523 ┆ 383.045872 ┆ 429.678899 ┆ 297.605505 │
        │ GOOG   ┆ Alphabet (Google) ┆ 152.669725 ┆ 153.779817 ┆ 151.174312 ┆ 177.348624 ┆ 111.431193 │
        │ AMZN   ┆ Amazon            ┆ 172.844037 ┆ 174.155963 ┆ 172.880734 ┆ 184.587156 ┆ 108.577982 │
        └────────┴───────────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘
        ```
        Notice how the behaviour of `with_columns` is slightly different here, since no Alias are provided it applies the operation on existing columns and returns the modified df.
    - Expansion using data type
        ```python
        result = df.with_columns((pl.col(pl.Float64, another_data_type) / eur_usd_rate).round(2))
        ```
        All columns of this type will be modified.
    - Expansion using regex
        Regex must start with ^ and end with $, that is what differentiates it from regular column name.
        ```python
        result = df.select(pl.col("ticker", "^.*_high$", "^.*_low$"))
        ```
    - `pl.all()` to select all columns. `pl.all().exclude('ticker', '^.*high$') or pl.col(pl.Float64).exclude('ticker', '^.*high$')` to exclude columns
    - column renaming 
    <br>
        This results an output df where there is same name
        ```python
        result = df.select(pl.col('company_name'))
        ```
        We can rename using either alias or prefix/suffix.
        ```python
        result = df.select(
            (pl.col("price") / gbp_usd_rate).alias("price (GBP)"),
            (pl.col("^year_.*$") / eur_usd_rate).name.prefix("in_eur_"),
            (pl.col("day_high", "day_low") / gbp_usd_rate).name.suffix("_gbp"),
        )
        ```
        Or we can pass a callable function to name.map()
        ```python
        result = df.select(pl.all().name.map(str.upper))
        ```
    - polars selectors
        ```python
        import polars.selectors as cs
        ```
        Selectors provide a bunch of selectors depending on the datatype.
        For example:
        ```python
        result = df.select(cs.string() | cs.ends_with("_high"))
        # Selects all string columns and then checks the ones which end with _high
        ```


### Polars optimized examples
Instead of doing this
```python
result = df
for tp in ["day", "year"]:
    result = result.with_columns(
        (pl.col(f"{tp}_high") - pl.col(f"{tp}_low")).alias(f"{tp}_amplitude")
    )
```
Do this
```python
def amplitude_expressions(time_periods):
    for tp in time_periods:
        yield (pl.col(f"{tp}_high") - pl.col(f"{tp}_low")).alias(f"{tp}_amplitude")


result = df.with_columns(amplitude_expressions(["day", "year"]))
```
It gives the same final result, but in second sample we generate the expression first and use it in a context, which helps parallelize things.
