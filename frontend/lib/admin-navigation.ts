import {
  BrainCircuit,
  ChartColumn,
  Cpu,
  Files,
  FolderTree,
  LayoutDashboard,
  Settings,
  Upload,
  Users,
  type LucideIcon,
} from "lucide-react";

export interface NavItem {
  title: string;
  href: string;
  icon: LucideIcon;
}

export interface NavGroup {
  title: string;
  items: NavItem[];
}

export const consoleNavigation: NavGroup[] = [
  {
    title: "General",
    items: [
      {
        title: "Dashboard",
        href: "/admin/dashboard",
        icon: LayoutDashboard,
      },
    ],
  },
  {
    title: "Knowledge Center",
    items: [
      {
        title: "Assets",
        href: "/admin/assets",
        icon: Files,
      },
      {
        title: "Upload",
        href: "/admin/upload",
        icon: Upload,
      },
    ],
  },
  {
    title: "Management",
    items: [
      {
        title: "Users",
        href: "/admin/users",
        icon: Users,
      },
      {
        title: "Analytics",
        href: "/admin/analytics",
        icon: ChartColumn,
      },
      {
        title: "Settings",
        href: "/admin/settings",
        icon: Settings,
      },
    ],
  },
];