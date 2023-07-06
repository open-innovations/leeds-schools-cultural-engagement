import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import metas from "lume/plugins/metas.ts";
import postcss from "lume/plugins/postcss.ts";

// Importing the OI Lume charts and utilities
import oiCharts from "https://deno.land/x/oi_lume_viz@v0.10.1/mod.ts";
import autoDependency from "https://deno.land/x/oi_lume_utils@v0.3.0/processors/auto-dependency.ts";
import csvLoader from "https://deno.land/x/oi_lume_utils@v0.3.0/loaders/csv-loader.ts";
import jsonLoader from "lume/core/loaders/json.ts";

const site = lume({
  src: './src',
  // TODO Update this with the proper URL
  location: new URL("https://open-innovations.github.io/leeds-schools-cultural-engagement/"),
});

// Register a series of extensions to be loaded by the OI CSV loader
// https://lume.land/docs/core/loaders/
site.loadData([".csv", ".tsv", ".dat"], csvLoader);
site.loadData([".geojson"], jsonLoader);

// Register an HTML processor
// https://lume.land/docs/core/processors/
site.process([".html"], autoDependency);

// Import lume charts
site.use(oiCharts({
	"colour": {
		"names": {
			"Academy & Free Schools": "#F7AB3D",
			"Voluntary": "#4A783C",
			"Community": "#69C2C9",
			"Independent": "#7D2248",
			"Foundation": "#005776",
			"Special School": "#FF808B",
			"Primary": "#f2e61a",
			"Secondary": "#636aaf",
			"Overall": "#19bc9c",
			"School/teachers": "#D50C52",
			"External providers": "#2DB8C5",
			"Key Stage 1": "#CBF8EF",
			"Key Stage 2": "#62EACF",
			"Key Stage 3": "#19BC9C",
			"Key Stage 4": "#138D75",
			"Key Stage 5": "#0D5E4E"
		}
	}
}));
site.use(base_path());
site.use(metas({
  defaultPageData: {
    title: 'title', // Use the `date` value as fallback.
  },
}));
site.use(date());
site.use(postcss({}));

site.copy('CNAME');
site.copy('.nojekyll');

export default site;
