import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from service.sql_execution_service import SQLExecutionResult

class ChartService:
    def generate_chart(self, execution_result: SQLExecutionResult) -> go.Figure | None:
        if execution_result.error or execution_result.row_count == 0:
            return None
            
        df = pd.DataFrame(execution_result.rows, columns=execution_result.columns)
        
        if len(df.columns) < 2:
            return None
            
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        
        if len(numeric_cols) == 0:
            return None
            
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            x_col = categorical_cols[0]
            y_col = numeric_cols[0]
            
            # Simple heuristic
            if df[x_col].nunique() <= 5 and df[y_col].min() >= 0:
                return px.pie(df, names=x_col, values=y_col, title=f"{y_col} by {x_col}")
            else:
                return px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                
        elif len(numeric_cols) >= 2:
            x_col = numeric_cols[0]
            y_col = numeric_cols[1]
            return px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
            
        return None
