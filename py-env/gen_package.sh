#!/bin/bash

package_dir="hms-mad"
rm -rf ${package_dir}
mkdir -p ${package_dir}

echo "Copying HMS MAD-I package contents"
cp -r README.md \
    hms-frontend \
    hms-backend \
    docs/hms-openapi-spec.yaml \
	docs/hms-mad-1-project-report.pdf \
    py-env \
    sql \
    ${package_dir}

echo "Creating the package"
zip -qr project_24f2005905.zip ${package_dir}

