import tempfile
from neo4j import GraphDatabase
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network


st.set_page_config(
    page_title="E-Commerce Graph Engine & Analytics", layout="wide"
)


# Sidebar Configuration
st.sidebar.title("🔌 Neo4j Aura Cloud Connection")
uri = st.sidebar.text_input("Neo4j URI", "neo4j+s://5acc955e.databases.neo4j.io")
user = st.sidebar.text_input("Username", "5acc955e")
password = st.sidebar.text_input(
    "Password", "XDGDCV7tjsy7otebyWiLnDf08LExdQZ6X0pG43X3h8M", type="password"
)
database_name = st.sidebar.text_input("Database Name", "5acc955e")




class GraphEngine:


  def __init__(self, uri, user, password, database="5acc955e"):
    self.driver = GraphDatabase.driver(uri, auth=(user, password))
    self.database = database if database else "5acc955e"


  def close(self):
    self.driver.close()


  def query(self, cypher, parameters=None):
    try:
      with self.driver.session(database=self.database) as session:
        result = session.run(cypher, parameters)
        return [record.data() for record in result]
    except Exception as e:
      st.error(f"Database Query Error: {e}")
      return []




db = None
try:
  db = GraphEngine(uri, user, password, database_name)
  st.sidebar.success("Connected to Neo4j Aura Cloud!")
except Exception as e:
  st.sidebar.error(f"Connection Failed: {e}")


st.title("🛍️ E-Commerce Graph Engine: CRUD, Analytics & Payment Insights")


# Database Reset Utility
st.sidebar.markdown("---")
st.sidebar.subheader("⚠️ Database Reset")
if st.sidebar.button("🧹 Clear Entire Graph Data"):
  if db:
    db.query("MATCH (n) DETACH DELETE n")
    st.sidebar.warning("Database cleared! Start inserting fresh nodes.")


# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "✏️ Dynamic CRUD Operations",
    "🕸️ Live Graph Visualizer",
    "💡 Recommendation Engine",
    "📊 Sales & Payment Analytics",
])




def get_existing_nodes():
  if db:
    res = db.query(
        "MATCH (n) RETURN DISTINCT coalesce(n.name, n.id) AS node_id ORDER BY"
        " node_id"
    )
    return [r["node_id"] for r in res if r.get("node_id")]
  return []




def get_existing_orders():
  if db:
    res = db.query(
        "MATCH (o:Order) RETURN DISTINCT coalesce(o.name, o.id) AS order_id"
        " ORDER BY order_id"
    )
    return [r["order_id"] for r in res if r.get("order_id")]
  return []




existing_nodes = get_existing_nodes()


# ---------------------------------------------------------
# TAB 1: ADVANCED DYNAMIC CRUD WITH COMBINED ORDER ENTRY
# ---------------------------------------------------------
with tab1:
  st.header("✏️ Advanced Entity CRUD Operations")


  crud_mode = st.radio(
      "Select CRUD Action:",
      [
          "➕ Create (Add Node/Edge)",
          "🔍 Read (Inspect Node)",
          "✏️ Update (Modify Property)",
          "🗑️ Delete (Remove Node)",
      ],
      horizontal=True,
  )


  payment_options = [
      "UPI",
      "Cash on Delivery (COD)",
      "Credit Card",
      "Debit Card",
      "Net Banking",
      "Online Credit / Pay Later",
  ]
  delivery_options = [
      "Standard Shipping",
      "Express Delivery",
      "Same-Day Delivery",
      "Pickup Point",
  ]


  # --- CREATE ---
  if crud_mode == "➕ Create (Add Node/Edge)":
    creation_type = st.radio(
        "Select Entity Creation Mode:",
        [
            "🛒 Complete Order Entry (Customer ➔ Order ➔ Payment)",
            "🔗 Standard Connection (Any Node to Any Node)",
            "💳 Payment Mode Link (Order ➔ PaymentMode)",
            "🚚 Delivery Mode Link (Order ➔ DeliveryMode)",
        ],
        horizontal=False,
    )


    # 1. Complete Order Entry Mode
    if creation_type == "🛒 Complete Order Entry (Customer ➔ Order ➔ Payment)":
      st.subheader("🛒 Fast Checkout Entry")
      col_c1, col_c2, col_c3 = st.columns(3)
      with col_c1:
        cust_id = st.text_input("👤 Customer Name", "Rohan")
      with col_c2:
        ord_id = st.text_input("📦 Order ID", "ORD_901")
      with col_c3:
        pay_mode = st.selectbox("💳 Payment Method", payment_options)
       
      if st.button("🚀 Create Full Order Record"):
        if db and cust_id and ord_id and pay_mode:
          cypher = """
          MERGE (c:Customer {id: $c_id, name: $c_id})
          MERGE (o:Order {id: $o_id, name: $o_id})
          MERGE (pm:PaymentMode {id: $p_mode, name: $p_mode})
          MERGE (c)-[:PLACED]->(o)
          MERGE (o)-[:PAID_VIA]->(pm)
          """
          db.query(cypher, {"c_id": cust_id, "o_id": ord_id, "p_mode": pay_mode})
          st.success(f"✅ Success: {cust_id} ➔ PLACED ➔ {ord_id} ➔ PAID_VIA ➔ {pay_mode}")
        else:
          st.warning("Please fill all fields.")


    # 2. Standard Connection Mode
    elif creation_type == "🔗 Standard Connection (Any Node to Any Node)":
      col1, col2, col3 = st.columns(3)
      with col1:
        src_label = st.selectbox("Source Label", ["Customer", "Order", "Product", "Category", "User"])
        src_id = st.text_input("Source Node Name / ID", "Product_A")
      with col2:
        rel_type = st.selectbox("Relationship (Edge)", ["PLACED", "CONTAINS", "BELONGS_TO", "LIKES", "RECOMMENDED"])
      with col3:
        tgt_label = st.selectbox("Target Label", ["Order", "Product", "Category", "Customer"])
        tgt_id = st.text_input("Target Node Name / ID", "Category_1")


      if st.button("🚀 Execute Create Query"):
        if db and src_id and tgt_id:
          cypher_cmd = f"""
                    MERGE (a:`{src_label.strip()}` {{id: $src_id, name: $src_id}})
                    MERGE (b:`{tgt_label.strip()}` {{id: $tgt_id, name: $tgt_id}})
                    MERGE (a)-[r:`{rel_type.strip().upper()}`]->(b)
                    """
          db.query(cypher_cmd, {"src_id": src_id, "tgt_id": tgt_id})
          st.success(f"Created Link: ({src_label}: {src_id}) ──[{rel_type}]──> ({tgt_label}: {tgt_id})")


    # 3. Payment Mode Link Mode
    elif creation_type == "💳 Payment Mode Link (Order ➔ PaymentMode)":
      col_p1, col_p2 = st.columns(2)
      orders_list = get_existing_orders()
      with col_p1:
        p_order_id = st.selectbox("Select Order ID", orders_list) if orders_list else st.text_input("Enter Order ID", "ORD_801")
      with col_p2:
        selected_payment = st.selectbox("Select Payment Method", payment_options)


      if st.button("💳 Link Payment Mode to Order"):
        if db and p_order_id and selected_payment:
          cypher_pay = """
                    MERGE (o:Order {id: $ord_id, name: $ord_id})
                    MERGE (pm:PaymentMode {id: $pay_mode, name: $pay_mode})
                    MERGE (o)-[r:PAID_VIA]->(pm)
                    """
          db.query(cypher_pay, {"ord_id": p_order_id, "pay_mode": selected_payment})
          st.success(f"Successfully Linked: Order {p_order_id} ──[PAID_VIA]──> {selected_payment}")


    # 4. Delivery Mode Link Mode
    elif creation_type == "🚚 Delivery Mode Link (Order ➔ DeliveryMode)":
      col_d1, col_d2 = st.columns(2)
      orders_list = get_existing_orders()
      with col_d1:
        d_order_id = st.selectbox("Select Order ID", orders_list) if orders_list else st.text_input("Enter Order ID", "ORD_801")
      with col_d2:
        selected_delivery = st.selectbox("Select Delivery Method", delivery_options)


      if st.button("🚚 Link Delivery Mode to Order"):
        if db and d_order_id and selected_delivery:
          cypher_del = """
                    MERGE (o:Order {id: $ord_id, name: $ord_id})
                    MERGE (dm:DeliveryMode {id: $del_mode, name: $del_mode})
                    MERGE (o)-[r:DELIVERED_VIA]->(dm)
                    """
          db.query(cypher_del, {"ord_id": d_order_id, "del_mode": selected_delivery})
          st.success(f"Successfully Linked: Order {d_order_id} ──[DELIVERED_VIA]──> {selected_delivery}")


  # --- READ ---
  elif crud_mode == "🔍 Read (Inspect Node)":
    if existing_nodes:
      selected_node = st.selectbox("Select Node to Inspect:", existing_nodes)
      if st.button("Fetch Node Details") and db:
        res = db.query(
            """
                MATCH (n) WHERE n.id = $q OR n.name = $q
                OPTIONAL MATCH (n)-[r]-(connected)
                RETURN labels(n)[0] AS Label, properties(n) AS Properties,
                       type(r) AS Relationship, coalesce(connected.name, connected.id) AS Connected_Node
                """,
            {"q": selected_node},
        )
        if res:
          st.dataframe(pd.DataFrame(res), use_container_width=True)
        else:
          st.info("No connections found for this node.")


  # --- UPDATE ---
  elif crud_mode == "✏️ Update (Modify Property)":
    if existing_nodes:
      target_node = st.selectbox("Select Target Node:", existing_nodes)
      col_u1, col_u2 = st.columns(2)
      with col_u1:
        prop_key = st.text_input("Property Name (e.g., status, amount, provider)", "status")
      with col_u2:
        prop_val = st.text_input("New Value", "Completed")


      if st.button("Update Property Value") and db:
        db.query(f"MATCH (n) WHERE n.id = $id OR n.name = $id SET n.`{prop_key}` = $val", {"id": target_node, "val": prop_val})
        st.success(f"Updated '{target_node}' -> property '{prop_key}' = '{prop_val}'")


  # --- DELETE ---
  elif crud_mode == "🗑️ Delete (Remove Node)":
    if existing_nodes:
      del_node = st.selectbox("Select Node to Delete:", existing_nodes)
      if st.button("Confirm Delete") and db:
        db.query("MATCH (n) WHERE n.id = $id OR n.name = $id DETACH DELETE n", {"id": del_node})
        st.error(f"Node '{del_node}' and all its connections deleted!")


# ---------------------------------------------------------
# TAB 2: LIVE GRAPH VISUALIZER
# ---------------------------------------------------------
with tab2:
  st.header("🕸️ Real-time Graph Network Visualizer")
  if db:
    if st.button("🔄 Render Interactive Network Canvas"):
      graph_data = db.query("""
                MATCH (a)-[r]->(b)
                RETURN labels(a)[0] AS source_type, coalesce(a.name, a.id) AS source,
                       type(r) AS rel,
                       labels(b)[0] AS target_type, coalesce(b.name, b.id) AS target
                LIMIT 150
            """)
      if graph_data:
        net = Network(height="550px", width="100%", directed=True, bgcolor="#1e1e1e", font_color="white")
        for row in graph_data:
          net.add_node(str(row["source"]), label=f"{row['source_type']}: {row['source']}")
          net.add_node(str(row["target"]), label=f"{row['target_type']}: {row['target']}")
          net.add_edge(str(row["source"]), str(row["target"]), title=row["rel"])
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
          net.save_graph(tmp.name)
          components.html(open(tmp.name, "r").read(), height=580)
      else:
        st.warning("Graph canvas is currently empty.")


# ---------------------------------------------------------
# TAB 3: GRAPH RECOMMENDATION ENGINE
# ---------------------------------------------------------
with tab3:
  st.header("💡 Collaborative Graph Recommendation Engine")
  if db:
    cust_list = [
        r["name"]
        for r in db.query(
            "MATCH (c:Customer) RETURN coalesce(c.name, c.id) AS name"
        )
    ]
    if cust_list:
      selected_cust = st.selectbox(
          "Select Customer for Product Recommendation:", cust_list
      )
      if st.button("✨ Find Best Recommendations"):
        # Updated Query for Recommendation Engine
        rec_cypher = """
                MATCH (c:Customer)-[:PLACED]->(:Order)-[:CONTAINS]->(p1:Product)
                WHERE c.name = $cust OR c.id = $cust
                MATCH (other:Customer)-[:PLACED]->(:Order)-[:CONTAINS]->(p1)
                WHERE other <> c
                MATCH (other)-[:PLACED]->(:Order)-[:CONTAINS]->(p2:Product)
                WHERE p1 <> p2 AND NOT (c)-[:PLACED]->(:Order)-[:CONTAINS]->(p2)
                RETURN p2.name AS Recommended_Product, count(DISTINCT other) AS Bought_By_Similar_Customers
                ORDER BY Bought_By_Similar_Customers DESC LIMIT 5
                """
        recs = db.query(rec_cypher, {"cust": selected_cust})
        if recs:
          st.success(f"Recommended Products for '{selected_cust}':")
          st.dataframe(pd.DataFrame(recs), use_container_width=True)
        else:
          st.info(
              f"No collaborative history found for '{selected_cust}'. Please ensure other customers have bought similar products."
          )
    else:
      st.info("No Customer nodes found. Add customers in CRUD tab first.")


# ---------------------------------------------------------
# TAB 4: SALES & MOST USED PAYMENT METHOD ANALYTICS
# ---------------------------------------------------------
with tab4:
  st.header("📊 Business Analytics & Payment Insights")


  if db:
    col_a1, col_a2 = st.columns(2)


    with col_a1:
      st.subheader("🏆 Best Selling Products")
      best_sellers = db.query("""
            MATCH (o:Order)-[:CONTAINS]->(p:Product)
            RETURN p.name AS Product_Name, count(o) AS Total_Orders
            ORDER BY Total_Orders DESC
            """)
      if best_sellers:
        df_bs = pd.DataFrame(best_sellers)
        st.metric("🥇 #1 Best Seller", df_bs.iloc[0]["Product_Name"], f"{df_bs.iloc[0]['Total_Orders']} Orders")
        fig_prod = px.bar(df_bs, x="Product_Name", y="Total_Orders", color="Total_Orders", title="Product Sales Volume")
        st.plotly_chart(fig_prod, use_container_width=True)
      else:
        st.info("No Product-Order sales data available.")


    with col_a2:
      st.subheader("💳 Most Used Payment Methods")
      payment_data = db.query("""
            MATCH (o:Order)-[:PAID_VIA]->(pm:PaymentMode)
            RETURN coalesce(pm.name, pm.id) AS Payment_Method, count(o) AS Usage_Count
            ORDER BY Usage_Count DESC
            """)
      if payment_data:
        df_pm = pd.DataFrame(payment_data)
        st.metric("⚡ Most Preferred Payment Mode", df_pm.iloc[0]["Payment_Method"], f"{df_pm.iloc[0]['Usage_Count']} Transactions")
        fig_pm = px.pie(df_pm, names="Payment_Method", values="Usage_Count", hole=0.4, title="Payment Method Distribution")
        st.plotly_chart(fig_pm, use_container_width=True)
      else:
        st.info("No Payment relationship data (PAID_VIA) available.")
       
    st.markdown("---")
    st.subheader("🔍 Complete Transaction Chain Breakdown")
    full_breakdown = db.query("""
        MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
        OPTIONAL MATCH (o)-[:PAID_VIA]->(pm:PaymentMode)
        OPTIONAL MATCH (o)-[:DELIVERED_VIA]->(dm:DeliveryMode)
        RETURN coalesce(c.name, c.id) AS Customer,
               coalesce(o.name, o.id) AS Order_ID,
               coalesce(p.name, p.id) AS Product,
               coalesce(pm.name, pm.id) AS Payment_Mode,
               coalesce(dm.name, dm.id) AS Delivery_Mode
        """)
    if full_breakdown:
      st.dataframe(pd.DataFrame(full_breakdown), use_container_width=True)
    else:
      st.info("No full customer transaction chain found.")

