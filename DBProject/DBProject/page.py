def page(table1, table2, table3, table4):
    a = 0
    b = 0
    c = 0
    d = 0
    page = """
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        </head>
        <body>
                <div style="float:left; margin: 0px 100px 100px 50px;">
                <h2>Elements</h2>
                <div style="height: 500px; overflow:auto;">
                <table border="1">
                    <tr>
                        <th width="1">Element ID</th>
                        <th>Element Name</th>
                    </tr>
                    """
    for var in table1:
        a += 1
        page += """
                    <tr>
                        <td width="1"> """ + str(var.element_id) + """ </td>
                        <td> """ + var.element_name + """ </td>
                    </tr>
                    """
        if a >= 1000:
            break

    page += """
                </table>
                </div>
                </div>

                <div style="float:left; margin: 0px 100px 100px 50px;">
                <h2>Hierarchy</h2>
                <div style="height: 500px; overflow:auto;">
                <table border="1">
                    <tr>
                        <th>Parent ID</th>
                        <th>Child ID</th>
                    </tr>
                """
    for var in table2:
        b += 1
        page += """
                    <tr>
                        <td> """ + str(var.parent_id) + """ </td>
                        <td> """ + str(var.child_id.element_id) + """ </td>
                    </tr>
                    """
        if b >= 1000:
            break

    page += """
                </table>
                </div>
                </div>

                <div style="float:left; margin: 0px 100px 100px 50px;">
                <h2>Attributes</h2>
                <div style="height: 500px; overflow:auto;">
                <table border="1">
                    <tr>
                        <th width="1">Element ID</th>
                        <th>Key</th>
                        <th>Value</th>
                    </tr>
                """
    for var in table3:
        c += 1
        page += """
                    <tr>
                        <td width="1"> """ + str(var.element_id) + """ </td>
                        <td> """ + str(var.key) + """ </td>
                        <td> """ + str(var.value) + """ </td>
                    </tr>
                    """
        if c >= 1000:
            break

    page += """
                </table>
                </div>
                </div>

                <div style="float:left; margin: 50px 100px 100px 50px;">
                <h2>Contents</h2>
                <div style="height: 500px; overflow:auto;">
                <table border="1">
                    <tr>
                        <th width="1">Element ID</th>
                        <th>Content</th>
                    </tr>
                """
    for var in table4:
        d += 1
        page += """
                    <tr>
                        <td width="1"> """ + str(var.element_id) + """ </td>
                        <td> """ + str(var.contents) + """ </td>
                    </tr>
                    """
        if d >= 1000:
            break

    page += """
                </table>
                </div>
                </div>            
    """
        # </body>
    # </html>
    # """

    page += """
    <div class="row" style="margin-bottom:200px;">
        <form action="/back">
            <div class="col-sm-12">
                <center><button class="btn btn-primary" style="height: 40px; width: 200px;" type="submit" value="Back">Back</button></center>
            </div>  
        </form>
    </div>
        </body>
    </html>
    """
    return page