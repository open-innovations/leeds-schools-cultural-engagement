import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import metas from "lume/plugins/metas.ts";
import postcss from "lume/plugins/postcss.ts";
import nunjucks from "lume/plugins/nunjucks.ts";
import inline from "lume/plugins/inline.ts";

// Importing the OI Lume charts and utilities
import oiCharts from "https://deno.land/x/oi_lume_viz@v0.16.11/mod.ts";
import autoDependency from "https://deno.land/x/oi_lume_utils@v0.3.0/processors/auto-dependency.ts";
import csvLoader from "https://deno.land/x/oi_lume_utils@v0.3.0/loaders/csv-loader.ts";
import jsonLoader from "lume/core/loaders/json.ts";

const site = lume({
  src: './src',
  // TODO Update this with the proper URL
  location: new URL("https://open-innovations.github.io/leeds-schools-cultural-engagement/"),
});

site.use(nunjucks());
site.use(inline(/* Options */));

// Register a series of extensions to be loaded by the OI CSV loader
// https://lume.land/docs/core/loaders/
site.loadData([".csv", ".tsv", ".dat"], csvLoader);
site.loadData([".geojson"], jsonLoader);

// Register an HTML processor
// https://lume.land/docs/core/processors/
site.process([".html"], (pages) => pages.forEach(autoDependency));

// Import lume charts
import oiChartsConfig from "./oi-charts-config.js";
site.use(oiCharts(oiChartsConfig));
site.use(base_path());
site.use(metas({
  defaultPageData: {
    title: 'title', // Use the `date` value as fallback.
  },
}));
site.use(date());
site.use(postcss({}));

// Copy orgs file to use in visualisation
site.remoteFile("_data/viz/organisations/orgs.csv","./data/orgs.csv");


// Section to process catalogue
import { parse } from "jsr:@std/yaml";
const yaml = await Deno.readTextFile("./src/catalogue/_data.yml");
const catalogue = parse(yaml);
catalogue.entries.forEach((entry: any) => {
	site.remoteFile(entry.download,"."+entry.data);
});
site.copy(['.csv']);





site.copy('CNAME');
site.copy('assets/images');
site.copy('.nojekyll');
site.copy([".woff2"]);
site.copy([".png"]);
site.copy([".js"]);
site.copy([".csv"]);


site.data('build', {
  date: new Date(),
  env: Deno.env.get('DENO_ENV')
});

export default site;
