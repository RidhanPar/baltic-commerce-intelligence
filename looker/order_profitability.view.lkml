view: order_profitability {
  sql_table_name: analytics.mart_order_profitability ;;

  dimension: order_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.order_id ;;
  }

  dimension_group: order {
    type: time
    timeframes: [date, week, month, quarter, year]
    sql: ${TABLE}.order_date ;;
  }

  dimension: market {
    type: string
    sql: ${TABLE}.market ;;
  }

  dimension: acquisition_channel {
    type: string
    sql: ${TABLE}.acquisition_channel ;;
  }

  measure: orders {
    type: count_distinct
    sql: ${order_id} ;;
  }

  measure: net_revenue {
    type: sum
    sql: ${TABLE}.net_revenue ;;
    value_format_name: eur
  }

  measure: contribution_margin {
    type: sum
    sql: ${TABLE}.contribution_margin ;;
    value_format_name: eur
  }

  measure: contribution_margin_percent {
    type: number
    sql: ${contribution_margin} / NULLIF(${net_revenue}, 0) ;;
    value_format_name: percent_1
  }
}

