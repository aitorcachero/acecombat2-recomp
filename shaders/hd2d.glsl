// 3D Crystal-Clear Full-Screen Shader for Ace Combat 2
// Rich vibrant colors, deep sky/ocean contrast, and silky-smooth water rendering.

vec3 sampleColor(vec2 uv) {
    return texture(u_tex, clamp(uv, vec2(0.0), vec2(1.0))).rgb;
}

void main() {
    vec2 uv = v_uv;
    vec3 c = sampleColor(uv);

    // Color Tone Curve & Mild Contrast Expansion
    c = (c - 0.5) * 1.05 + 0.5;
    c = clamp(c, 0.0, 1.0);

    // Selective Vibrance Enhancement (deep blue skies and vivid explosions)
    float luma = dot(c, vec3(0.299, 0.587, 0.114));
    float maxCol = max(max(c.r, c.g), c.b);
    float minCol = min(min(c.r, c.g), c.b);
    float sat = maxCol - minCol;
    float vibrance = 0.20;
    c = mix(vec3(luma), c, 1.0 + vibrance * (1.0 - sat));

    o = vec4(clamp(c, 0.0, 1.0), 1.0);
}
