APP_LANG = {
    "中文": {
        "title": "📦 仓储选址算法平台",
        "welcome":"欢迎使用！请通过左侧导航栏选择功能页面：",
        "navigation": """
        ### 📘 页面导航说明：
        - **项目背景**：了解问题背景
        - **执行算法**：了解输入输出文件格式，编辑输入文件，运行算法并查看结果
        """
    },
    "English": {
        "title": "📦 Warehouse Location Optimization Platform",
        "welcome":"Welcome! Please use the sidebar to navigate between pages:",
        "navigation": """
        ### 📘 Page Navigation Guide:
        - **Project Background**: Understand the problem context
        - **Run Algorithm**: Learn input/output formats, edit input files, run the algorithm and view results
        """
    }
    }

DOC_LANG = {
    "中文": {
        "title": "📦 仓储选址与库存优化系统 - 项目文档",
        "background_header": "📘 项目背景简介",
        "background_markdown": """
该项目旨在解决一个典型的供应链网络优化问题，目标是在满足客户需求和运输时效的前提下，**选择最优的仓储选址和库存配置方案**，以实现系统总成本最小化。

### 🎯 优化目标
- 决定在哪些候选城市设立仓库；
- 为每个仓库配置合适的库存；
- 确定每个客户的需求由哪个仓库供应及其供应量；
- 最终使得系统的 **总成本最小**。

### 📌 约束条件
- 未建仓城市不能存货；
- 总库存需控制在上下限之间；
- 每个仓库出货量不能超过库存；
- 每个客户的收货量不能超过其需求；
- 仓库总数需满足数量约束（最小/最大建仓数）；
- 仓库与客户城市之间运输时间存在上限。
"""
    },
    "English": {
        "title": "📦 Warehouse Location & Inventory Optimization - Documentation",
        "background_header": "📘 Project Background",
        "background_markdown": """
This project addresses a classic supply chain network optimization problem. The goal is to **select the optimal warehouse locations and inventory configurations** to minimize total system cost, while meeting customer demand and delivery time constraints.

### 🎯 Optimization Objectives
- Decide which candidate cities should host warehouses;
- Allocate appropriate inventory levels to each warehouse;
- Determine which warehouse supplies each customer and how much;
- Ultimately minimize the **total system cost**.

### 📌 Constraints
- No inventory in cities without warehouses;
- Total inventory must be within specified bounds;
- A warehouse cannot ship more than its inventory;
- A customer cannot receive more than its demand;
- The number of warehouses must meet min/max constraints;
- Delivery time between warehouse and customer must not exceed the limit.
"""
    }
}


ALGO_LANG = {
    "中文": {
        "title": "⚙️ 仓储选址算法",
        "intro": "请在“执行算法”页面将示例输入文件改成你需要的数据。",
        "input_doc": "📥 输入接口文档",
        "global_param_doc": "📥 输入文件说明：全局参数.csv",
        "param_enum": "参数枚举说明：",
        "demand_doc": "📥 输入文件说明：需求分布.csv",
        "supply_doc": "📥 输入文件说明：供应城市.csv",
        "distance_doc": "📥 输入文件说明：距离数据.csv",
        "output_doc": "📤 输出接口文档",
        "kpi_doc": "📊 输出文件说明：指标输出.csv",
        "kpi_enum": "常见指标说明：",
        "warehouse_doc": "📊 输出文件说明：构建仓库的城市输出.csv",
        "fulfill_doc": "📊 输出文件说明：需求城市满足情况输出.csv",
        "sample_data": "📄 示例输入数据（可编辑）",
        "edit_global": "📝 编辑全局参数",
        "edit_demand": "📝 编辑需求数据",
        "edit_supply": "📝 编辑供应城市",
        "edit_distance": "📝 编辑距离数据",
        "download": "📥 下载编辑后的 {}",
        "run_button": "🚀 运行算法",
        "running": "算法运行中，请稍候...",
        "success": "✅ 算法运行完成！共{}秒。",
        "error": "❌ 算法运行出错：{}",
        "output_result": "📊 输出结果"
    },
    "English": {
        "title": "⚙️ Warehouse Location Optimization",
        "intro": "Please modify the sample input files on the 'Run Algorithm' page.",
        "input_doc": "📥 Input Interface Documentation",
        "global_param_doc": "📥 Input File: Global Parameters.csv",
        "param_enum": "Parameter Enumeration:",
        "demand_doc": "📥 Input File: Demand Distribution.csv",
        "supply_doc": "📥 Input File: Supply Cities.csv",
        "distance_doc": "📥 Input File: Distance Data.csv",
        "output_doc": "📤 Output Interface Documentation",
        "kpi_doc": "📊 Output File: KPI Output.csv",
        "kpi_enum": "Common KPI Descriptions:",
        "warehouse_doc": "📊 Output File: Warehouse Cities.csv",
        "fulfill_doc": "📊 Output File: Demand Fulfillment.csv",
        "sample_data": "📄 Sample Input Data (Editable)",
        "edit_global": "📝 Edit Global Parameters",
        "edit_demand": "📝 Edit Demand Data",
        "edit_supply": "📝 Edit Supply Cities",
        "edit_distance": "📝 Edit Distance Data",
        "download": "📥 Download edited {}",
        "run_button": "🚀 Run Algorithm",
        "running": "Running algorithm, please wait...",
        "success": "✅ Algorithm completed! Time: {} seconds.",
        "error": "❌ Algorithm error: {}",
        "output_result": "📊 Output Results"
    }
}
