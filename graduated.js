// ==UserScript==
// @name         yanjiusheng
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  multiple classes supported
// @author       Jeffery
// @match        http://mis.teach.ustc.edu.cn/gradLoginSuc.do
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    //在这里添加你想要的课程号们，不限制个数
    var ids = ["CH6520501", "CH6620401", "CH2522301"];
    //在这里修改每多久查询一次，单位毫秒。不要过于频繁以免被服务器封禁。原为5000。
    var times = 5000;
    var got = [];
    for (var i = 0; i < ids.length; i++) {
        got.push(false);
    }
    var inter = setInterval(function() {
        var log_string = "";
        var table = frames["mainFrame"].frames["I2"].frames["xkpFrame"].document.children[0].children[1].children[0].children[0].children[2].children[0];
        for (var i = 0; i < ids.length; i++) {
            var line = get_line_with_id(table, ids[i]);
            var people = line.children[8];
            if (got[i] === false) {
                if (people.childNodes[0].data != (people.childNodes[3].innerText + "/")) {
                    frames["mainFrame"].frames["I2"].frames["xkpFrame"].xk(ids[i]);
                    got[i] = true;
                    alert("class" + toString(i) + " get!");
                } else {
                    log_string = log_string + line.children[3].children[0].innerText + " : " + people.childNodes[0].data + people.childNodes[3].innerText + "\n";
                    //console.log(line.children[3].children[0].innerText + " : " + people.childNodes[0].data + people.childNodes[3].innerText);
                }
            }
        }
        for (var i = 0; i < got.length; i++) {
            if (got[i] === false) {
                console.log(log_string);
                frames["mainFrame"].frames["I2"].frames["xkpFrame"].cxdxkc();
                return;
            }
        }
        clearInterval(inter);
        alert("all get!");
        return;
    }, times);

    function get_line_with_id(table, id) {
        for (i = 1; i < table.rows.length; i++) {
            if (table.rows[i].children[2].innerText == id) {
                return table.rows[i];
            }
        }
        return null;
    }
    // Your code here...
})();