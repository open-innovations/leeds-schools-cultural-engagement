# oi-lume-template


Welcome to the OI Lume Template.
You can see what this looks like by visiting 
<https://open-innovations.github.io/oi-lume-template/>.

You'll need to customise some things to get started:

* Review the contents of `_config.ts`. Pay particular attention to the site URL,
  as this will affect how relative links are created. You can probably ignore
  the rest of this for the moment.
* The source for the site is held in the `src` directory.
* Review the contents of `src/_data.yml`
    * This is where the default page layout is defined in the `layout` key.
      The default is `templates/page.njk`. This template can be found in the
      `_includes` directory.
    * Select colours for the site header and logo by updating the `logo_colour`
      and `header_class` keys. The [Open Innovations Brand page](https://open-innovations.org/brand/)
      will help.
    * Edit the site title and other SEO metadata in  under the
      `metas` key. See the [Lume metas plugin documentation](https://lume.land/plugins/metas/)
      for more information.
* Edit the title of this page in the frontmatter above. You can override the
  template by setting the `layout` key. 