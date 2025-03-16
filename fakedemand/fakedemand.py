from series import Row
import factors

r1 = Row(idx=1, factors=[factors.Sales(30, 0)])

r1.render_pandas_df('sales')

