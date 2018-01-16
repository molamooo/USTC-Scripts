var id = "204X0401";
var inter = setInterval(function() {
    var button = frames["main"].frames["dxkciframe"].document.dxform.childNodes[17].children["dxkccxtjtable"].rows[0].children[6].children[0];
    var table = frames["main"].frames["dxkciframe"].document.dxform.childNodes[17].children["dxkctable1"].children[0];
    var line = get_line_with_id(table, id);
    if (line == null) {
        alert("cannot find course!");
        button.click();
        return;
    }
    var people = line.children[8].innerText;
    var i = 0;
    for (; i < people.length; i++) {
        if (people[i] == '/') {
            var total_people = people.substring(0, i);
            i++;
            break;
        }
    }
    for (; i < people.length; i++) {
        if (people[i] == '/') {
            var current_people = people.substring(i + 1, people.length);
            break;
        }
    }
    if (total_people == current_people) {
        button.click();;
        return;
    }

    line.children[10].children[0].click();
    alert("available & already got it!");
    clearInterval(inter);
    /*
    var table_want = frames["main"].frames["xdkciframe"].document.gwcform.childNodes[37].children["xdkctable1"];
    var line_want = get_line_with_id(table_want, id);
    if (line == null) {
        alert("mistake! found available but couldn't find it to confirm");
        return;
    }
    lind.children[0].children[1].click();

    button.click();
    */
}, 5000)
function get_line_with_id(table, id) {
    for (i = 1; i < table.rows.length; i++) {
        if (table.rows[i].children[1].innerText == id) {
            return table.rows[i];
        }
    }
    return null;
}
