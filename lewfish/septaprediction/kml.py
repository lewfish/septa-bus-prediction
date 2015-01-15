"""Some code for dealing with SEPTA KML files. Not currently being used."""

import lxml.etree as etree
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def parse_kml(fn):
    """Parses a SEPTA route KML file into a list of lat/lons."""
    root = etree.parse(fn)
    #    print(etree.tostring(root, pretty_print=True))
    line_strs = root.xpath("//s:LineString//s:coordinates//text()",
                       namespaces={'s':"http://www.opengis.net/kml/2.2"})
    
    lines = []
    for l in line_strs:
        float_strs = re.findall(r"(-?\d+(.\d+)?)", l)
        line = tuple([float(f[0]) for f in float_strs])
        lines.append(line)
    return lines

def test_parse_kml():
    """Parses a KML file and plots the coordinates"""
    def plot_lines(lines):
        for i,l in enumerate(lines):
            plt.plot([l[0], l[3]],
                     [l[1], l[4]],
                     color = cm.gist_rainbow(float(i) / float(len(lines))))
            plt.show()
            plt.close()

            for i,l in enumerate(lines):
                plt.scatter([l[3]],
                            [l[4]],
                            color = cm.gist_rainbow(float(i) / float(len(lines))))
            plt.show()
            plt.close()

    def plot_sorted_points(points):
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]

        print lats
    
        plt.plot(lats, lons)
        plt.show()
        plt.close()

    fn = "data/47.kml"
    lines = parse_kml(fn)

    plot_lines(lines)

    l_dict = {}
    for l in lines:
        a = (l[0], l[1])
        b = (l[3], l[4])
        l_dict[a] = b
        print a, b

    #first point
    a = (lines[1][0], lines[1][1])
    sorted_points = []
    for i in xrange(len(lines) - 1):
        b = l_dict[a]
        sorted_points.append(a)
        a = b

    plot_sorted_points(sorted_points)

if __name__ == "__main__":
    test_parse_kml()
