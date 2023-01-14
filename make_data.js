// get the data from scraped_data.json file
// and extract products from categories
const fs = require('fs')
const path = require('path')

function makeUrlFriendly(name) {
    // convert name to url friendly name
    // eg:   'Hand Protection' -> 'hand-protection',

    // 1. trim ( remove leading and trailing spaces )
    // 2. replace space with '-'
    // 3. convert to lowercase
    return name.trim().replace(/ /g, '-').toLowerCase()
}

function import_json(name) {
    const file = path.join(__dirname, name)
    const data = fs.readFileSync(file, 'utf8')
    return JSON.parse(data)
}

function export_json(name, data) {
    const file = path.join(__dirname, name)
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

const actions = {
    "generate": {
        "products": function () {
            function get_products() {
                const data = import_json('scraped_data.json').categories
                const products = []
                let id = 1
                /**
                 * {
                 *  id: number,
                 * title: name{string},
                 * description: description{string},
                 * img: image{string},
                 * images: images{array<
                 *  images {
                 *    image_id
                 *    id
                 *    alt
                 *    src
                 *  }
                 * >},
                 * price: price{number},
                 * category: string,
                 * }
                 */
                for (const category of data) {
                    for (const product of category.products) {
                        const images = []
                        for (const image of product.images) {
                            images.push({
                                src: image,
                                alt: product.name,
                                image_id: id,
                                id: id,
                            });
                        }
                        products.push({
                            id: id,
                            title: product.name,
                            description: product.description,
                            img: product.image,
                            images: images,
                            price: product.price,
                            category: makeUrlFriendly(category.name),
                        });
                        ++id;
                    }
                }
                return products
            }

            data = import_json('scraped_data.json')
            products = get_products()
            export_json('products.json', products)
        },
        "categories":
            function get_categories() {
                const data = import_json('scraped_data.json').categories
                const categories = []
                for (const category of data) {
                    categories.push(makeUrlFriendly(category.name));
                }
                return categories
            },
    },
    "filter": {
        "products": (args) => {
            const conditions = {};
            for (const arg of args) {
                const [key, value] = arg.split('=')
                try {
                    conditions[key] = JSON.parse(`{"value": ${value}}`).value
                } catch (e) {
                    console.log(e)
                    conditions[key] = value
                }
            }
            const filter = function (conditions) {
                const isAllowed = (product, conditions) => {
                    for (const key in conditions) {
                        if (key && !(key in product)) {
                            return false
                        }
                        if (typeof conditions[key] === 'string')
                            if (product[key] !== conditions[key]) {
                                return false
                            }
                        if (Array.isArray(conditions[key]))
                            if (!conditions[key].includes(product[key])) {
                                return false
                            }
                        return true
                    }
                }
                const products = import_json('products.json')
                const filtered_products = []
                for (const product of products) {
                    if (isAllowed(product, conditions)) {
                        filtered_products.push(product)
                    }
                }
                return filtered_products
            };
            return filter(conditions);
        },
    }
};

function main() {
    const process_args = process.argv.slice(2);
    if (process_args.length < 2) {
        console.log('Please provide action name')
        return
    }

    const action = process_args[0]
    const sub_action = process_args[1]
    const args = process_args.slice(2)
    if (action in actions) {
        const res = actions[action][sub_action](args)
        if (res) {
            console.log(res)
            export_json(`result_${action}_${sub_action}.json`, res)
        }
    }
}

main();