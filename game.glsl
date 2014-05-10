---vertex
$HEADER$

attribute vec2  vCenter;
attribute float vRotation;
attribute float vScale;
attribute float vOpacity;

void main(void)
{
    frag_color = vec4(1.0, 1.0, 1.0, vOpacity);
    tex_coord0 = vTexCoords0;
    float a_sin = sin(vRotation);
    float a_cos = cos(vRotation);
    mat4 rot_mat = mat4
        (a_cos, -a_sin, 0.0, 0.0,
         a_sin,  a_cos, 0.0, 0.0,
         0.0,    0.0,   1.0, 0.0,
         0.0,    0.0,   0.0, 1.0);
    mat4 trans_mat = mat4
        (1.0, 0.0, 0.0, vCenter.x,
         0.0, 1.0, 0.0, vCenter.y,
         0.0, 0.0, 1.0, 0.0,
         0.0, 0.0, 0.0, 1.0);
    vec4 pos = vec4(vPosition.xy * vScale, 0.0, 1.0);
    vec4 trans_pos = pos * rot_mat * trans_mat;
    gl_Position = projection_mat * modelview_mat * trans_pos;
}

---fragment
$HEADER$

void main(void)
{
    gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
}
