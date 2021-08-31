<script src="//d3.js.org/d3.vc.min.js" charset = "utf-8"></script>
<script src="//d3.js.org/topojson.v1.min.js"></script>

const ranking_json = require('./ranking_data_out.json')

var ranking_dict = {}

for(var i = 0; i < ranking_json.length; i++){
	var curr = ranking_json[i];

	var name = curr.name
	var rank = curr.Rank

	ranking_dict[name] = rank
}

d3.json("us.json", function(error,us){
	if(error) return console.error(error);
	console.log(us)
});

console.log(ranking_dict)