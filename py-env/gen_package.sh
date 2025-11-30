#!/bin/bash

package_dir="hms-mad"
rm -rf ${package_dir}
mkdir -p ${package_dir}

echo "Copying HMS MAD-I package contents"
cp -r README.md \
    hms-frontend \
    hms-backend \
    docs/hms-openapi-spec.yaml \
    py-env \
    sql \
    ${package_dir}

echo "Creating the package"
zip -qr hms-mad.zip ${package_dir}

