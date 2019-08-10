% rebase('views/base.tpl', title='Circle')
<span id="circleId" data-id="{{model.id}}" data-enrolled="{{model.enrolled}}" data-percent="{{round((model.enrolled * 100.0) / model.capacity)}}"></span>
<h1>{{model.name}}</h1>

<h2>Circle Information</h2>
There are currently {{model.enrolled}} of {{model.capacity}} people enrolled. There are {{model.capacity - model.enrolled}} seats left!

<div id="progress" style="margin: 25px;"></div>

<div id="circles_people" class="managerPane">

    <h2>People</h2>
    <div class="tables" id="circles_people-table">
        % include('views/item_table.tpl', items=items)
    </div>


    <div class="inputForm hidden" id="editForm-circles_people" data-add-route-params="{{model.id}},dom~circles_people-peopleid~val">

        <h2>People</h2>
        <div class="closeX">x</div>
        <div class="clear"></div>

        <label for="circles_people-peopleid">Person</label>
        <select class="event" name="circles_people-peopleid" id="circles_people-peopleid" data-domain="people-last"></select>
        <div class="clear"></div>

        <button type="button" class="submitButton" id="submit-circles_people">Save</button>
        <br /><br />

    </div>
    <div class="clear"></div>

</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script type="text/javascript" src="http://d3js.org/d3.v3.min.js"></script>
<link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:200' rel='stylesheet' type='text/css'>
<style type="text/css">
    text {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 60pt;
        fill: black;
    }
</style>

<script type="text/javascript">

    initialValCheck = 0;

    function makeData() {
        return d3.range(1).map(function (item) {
            //return Math.floor(Math.random() * 100) + 1;
            if (initialValCheck === 0) {
                initialValCheck = 1;
                return 1;
            }
            return $("#circleId").data("percent");
        });
    };

    var color = d3.scale.linear()
        .domain([0, 0.5, 1])
        .range(["red", "yellow", "green"]);


    var colorLock = {},
        arcLock = {};

    function paths(percentages) {
        return percentages.map(function (percent) {
            var degrees = (percent / 100) * 360.0;
            var radians = degrees * (Math.PI / 180);
            var data = { value: percent, startAngle: 0, endAngle: radians };
            return data;
        });
    }

    function path2(percent) {
        var degrees = (percent / 100) * 360.0;
        var paths = d3.range(1, degrees).map(function (degree) {
            var startRadians = (degree - 1) * (Math.PI / 180);
            var endRadians = degree * (Math.PI / 180);
            var data = { index: degree, value: percent, startAngle: startRadians, endAngle: endRadians };
            return data;
        })
        console.log(paths);
        return paths;
    }

    function pathName(path) { return path.data; }

    var w = 200, h = w;

    var outerRadius = w / 2;
    var innerRadius = (w / 2) * (80 / 100);
    var arc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius);

    //Create SVG element
    var svg = d3.select("#progress")
        .append("svg")
        .attr("width", w)
        .attr("height", h);

    var g = svg.append('g')
        .attr('transform', 'translate(' + w / 2 + ',' + h / 2 + ')');

    var percent = makeData();
    g.datum(percent).selectAll("path")
        .data(paths)
        .enter()
        .append("path")
        //.attr("fill", function(d){return (d.index%2==0)?"#B20100":"#F20100"})
        //.attr("fill", function(d){return color(d.value)})
        .attr("fill", "#fcb040")
        .attr("d", arc)
        .each(function (d) { this._current = d; });

    svg.datum(percent).selectAll("text")
        .data(paths)
        .enter()
        .append("text")
        .attr("length", "50pc")
        .attr("transform", function (d) {
            return "translate(" + w / 2 + ", " + h / 1.6 + ")";
        })
        .attr("text-anchor", "middle")
        .text(function (d) { return "d.value" });

    function render() {
        percent = makeData();
        g.datum(percent).selectAll("path").data(paths).transition().duration(1000).attrTween("d", arcTween);
        //g.datum(percent).selectAll("path").data(paths).transition().duration(1000).attrTween("fill", colTween);
        //svg.datum(percent).selectAll("text").data(paths).text("function (d) { return d.value; }");
        svg.datum(percent).selectAll("text").data(paths).text($("#circleId").data("enrolled"));
    }

    function arcTween(a) {
        var i = d3.interpolate(this._current, a);
        this._current = i(0);
        return function (t) {
            return arc(i(t));
        };
    }

    function colTween(final) {
        var interpTo = d3.interpolateRgb(this._color, color(final.value / 100));
        this._color = interpTo(1);
        return function (next) {
            return interpTo(next);
        };
    }

    render();
    setInterval(render, 2000);
</script>

<script type="text/javascript" src="/static/js/DataTables/datatables.min.js"></script>