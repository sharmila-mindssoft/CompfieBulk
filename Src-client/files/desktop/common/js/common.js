
//
// Name manipulation
// parseHyphenated, toUpperCamelCase, hyphenatedToUpperCamelCase
//

function parseHyphenated(name) {
    return name.split("-");
}

function toUpperCamelCase(parts) {
    var result = [];
    for (var i = 0; i < parts.length; ++i) {
        var s = parts[i];
        s = s[0].toUpperCase() + s.slice(1);
        result.push(s);
    }
    return result.join("");
}

function hyphenatedToUpperCamelCase(name) {
    var parts = parseHyphenated(name);
    return toUpperCamelCase(parts);
}