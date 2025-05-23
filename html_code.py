# html_code.py
def generate_html(checkbox_states):
    html = f"""
    <div class="container">
        <div class="row">
            <div class="col-12">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col">Select Day</th>
                            <th scope="col">Article Name</th>
                            <th scope="col">Author</th>
                            <th scope="col">Words</th>
                            <th scope="col">Shares</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="customCheck1" {"checked" if checkbox_states.get("check1") else ""}>
                                    <label class="custom-control-label" for="customCheck1">1</label>
                                </div>
                            </td>
                            <td>Bootstrap 4 CDN and Starter Template</td>
                            <td>Cristina</td>
                            <td>913</td>
                            <td>2.846</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="customCheck2" {"checked" if checkbox_states.get("check2") else ""}>
                                    <label class="custom-control-label" for="customCheck2">2</label>
                                </div>
                            </td>
                            <td>Bootstrap Grid 4 Tutorial and Examples</td>
                            <td>Cristina</td>
                            <td>1.434</td>
                            <td>3.417</td>
                        </tr>
                        <tr>
                            <td>
                                <div class="custom-control custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" id="customCheck3" {"checked" if checkbox_states.get("check3") else ""}>
                                    <label class="custom-control-label" for="customCheck3">3</label>
                                </div>
                            </td>
                            <td>Bootstrap Flexbox Tutorial and Examples</td>
                            <td>Cristina</td>
                            <td>1.877</td>
                            <td>1.234</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """
    return html